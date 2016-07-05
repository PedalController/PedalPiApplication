from architecture.privatemethod import privatemethod

from dao.BankDao import BankDao

from model.Bank import Bank
from model.UpdatesObserver import UpdateType

from controller.Controller import Controller
from controller.DeviceController import DeviceController
from controller.NotificationController import NotificationController


class BanksController(Controller):
    banks = None

    def configure(self):
        self.dao = self.app.dao(BankDao)
        self.banks = self.dao.all

        # To fix Cyclic dependece
        from controller.CurrentController import CurrentController
        self.currentController = self.app.controller(CurrentController)
        self.deviceController = self.app.controller(DeviceController)
        self.notificationController = self.app.controller(NotificationController)

    def createBank(self, bank):
        """
        @return bank index
        """
        bankModel = Bank(bank)

        self.banks.append(bankModel)
        self.dao.save(bankModel)
        self.notifyChange(bank, UpdateType.CREATED)

        return bankModel.index

    def updateBank(self, bank, data):
        self.dao.delete(bank)
        bank.json = data

        self.dao.save(bank)
        if self.currentController.isCurrentBank(bank):
            currentPatch = self.currentController.currentPatch
            self.deviceController.loadPatch(currentPatch)

        self.notifyChange(bank, UpdateType.UPDATED)

    def deleteBank(self, bank):
        if bank == self.currentController.currentBank:
            self.currentController.toNextBank()

        del self.banks[bank.index]
        self.dao.delete(bank)

        self.notifyChange(bank, UpdateType.DELETED)

    @privatemethod
    def notifyChange(self, bank, updateType):
        self.notificationController.notifyBankUpdate(bank, updateType)
