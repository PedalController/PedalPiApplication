# -*- coding: utf-8 -*-
from architecture.privatemethod import privatemethod

from dao.BankDao import BankDao

from model.Bank import Bank
from model.UpdatesObserver import UpdateType

from controller.Controller import Controller
from controller.DeviceController import DeviceController
from controller.NotificationController import NotificationController


class BanksController(Controller):
    """
    Manage :class:`Bank`, creating new, updating or deleting.
    """
    banks = None

    def configure(self):
        self.dao = self.app.dao(BankDao)
        self.banks = self.dao.all

        # To fix Cyclic dependece
        from controller.CurrentController import CurrentController
        self.currentController = self.app.controller(CurrentController)
        self.deviceController = self.app.controller(DeviceController)
        self.notificationController = self.app.controller(NotificationController)

    def createBank(self, bank, token=None):
        """
        Persists a new :class:`Bank` in database.

        :param dict bank: Bank content
        :param string token: Request token identifier
        :return int: bank index
        """
        bankModel = Bank(bank)

        self.banks.append(bankModel)
        self.dao.save(bankModel)
        self.notifyChange(bankModel, UpdateType.CREATED, token)

        return bankModel.index

    def updateBank(self, bank, data, token=None):
        """
        Update a :class:`Bank` object based in data parsed.

        .. note::
            If you're changing a bank that has a current patch,
            the patch should be fully charged. So, prefer the use of other
            Controllers for simple changes.

        :param Bank bank: Bank to be updated
        :param dict data: New data bank
        :param string token: Request token identifier
        :return int: bank index
        """
        self.dao.delete(bank)
        bank.json = data

        self.dao.save(bank)
        if self.currentController.isCurrentBank(bank):
            currentPatch = self.currentController.currentPatch
            self.deviceController.loadPatch(currentPatch)

        self.notifyChange(bank, UpdateType.UPDATED, token)

    def deleteBank(self, bank, token=None):
        """
        Remove the :class:`Bank` object parameter.

        .. note::
            If the Bank contains deleted contains the current patch,
            another patch will be loaded and it will be the new current patch.

        :param Bank bank: Bank to be updated
        :param string token: Request token identifier
        """
        if bank == self.currentController.currentBank:
            self.currentController.toNextBank()

        del self.banks[bank.index]
        self.dao.delete(bank)

        self.notifyChange(bank, UpdateType.DELETED, token)

    def swapBanks(self, bankA, bankB, token=None):
        """
        Deprecated

        Swap bankA index to bankB index
        """
        self.banks.swap(bankA, bankB)

        self.dao.save(bankA)
        self.dao.save(bankB)

        self.notifyChange(bankA, UpdateType.UPDATED, token)
        self.notifyChange(bankB, UpdateType.UPDATED, token)

    def swapPatches(self, patchA, patchB):
        """
        Deprecated

        Swap patchA order to patchB order
        """
        patchA.bank.swapPatches(patchA, patchB)
        self.dao.save(patchA.bank)

    @privatemethod
    def notifyChange(self, bank, update_type, token=None):
        self.notificationController.notifyBankUpdate(bank, update_type, token)
