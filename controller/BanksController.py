from dao.BankDao import BankDao

from model.Bank import Bank

from controller.Controller import Controller


class BanksController(Controller):
    '''
    For get bank/patch/effect of patch/param, use self.banks
    '''
    banks = None

    def configure(self):
        self.dao = self.app.dao(BankDao)
        self.banks = self.dao.all

        # To fix Cyclic dependece
        from controller.CurrentController import CurrentController
        self.currentController = self.app.controller(CurrentController)

    # ***********************************
    # Data CRUD
    # ***********************************
    def createBank(self, bank):
        bankModel = Bank(bank)

        self.banks.append(bankModel)
        self.dao.save(bankModel)

        return bankModel.index

    def updateBank(self, bank, data):
        self.dao.delete(bank)

        index = bank.data["index"]
        bank.json.clear()
        bank.json.update(data)
        bank.json["index"] = index

        self.dao.save(bank)

        print("BanksController: Chamar internamente DeviceController \
               para atualizar estado do dispositivo se for o atual")

    def deleteBank(self, bank):
        self.banks.delete(bank.data["index"])
        self.dao.delete(bank)
        print("BanksController: Chamar internamente DeviceController para \
              atualizar estado do dispositivo se for o atual")

    def createPatch(self, bank, patch):
        bank.addPatch(patch)
        print("Dao: salvar")
        print("Current: Chamar internamente CurrentController para \
              atualizar estado do dispositivo se for o atual")
        return len(bank.patches) - 1

    def updatePatch(self, bank, patchNumber, patch):
        bank.patches[patchNumber] = patch
        print("Current: Chamar internamente CurrentController para \
              atualizar estado do dispositivo se for o atual")
        print("Dao: salvar")
        self.currentController.setPatch(patch)

    def addEffect(self, bank, indexPatch, effect):
        bank.addEffect(indexPatch, effect)
        print("BanksController: Chamar internamente DeviceController\
               para atualizar estado do dispositivo se for o atual")
        return len(bank.getEffects(indexPatch)) - 1
