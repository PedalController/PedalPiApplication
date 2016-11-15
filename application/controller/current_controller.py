from application.controller.controller import Controller
from application.controller.banks_controller import BanksController
from application.controller.device_controller import DeviceController
from application.controller.effect_controller import EffectController
from application.controller.notification_controller import NotificationController
from application.controller.param_controller import ParamController

from dao.CurrentDao import CurrentDao


class CurrentController(Controller):
    """
    Manage the current :class:`Bank` and current :class:`Patch`
    """

    def __init__(self, application):
        super(CurrentController, self).__init__(application)
        self.dao = None
        self.bank_number = 0
        self.patch_number = 0

        self.device_controller = None
        self.banks_controller = None
        self.effect_controller = None
        self.notifier = None
        self.param_controller = None

    def configure(self):
        self.device_controller = self.app.controller(DeviceController)
        self.banks_controller = self.app.controller(BanksController)
        self.effect_controller = self.app.controller(EffectController)
        self.notifier = self.app.controller(NotificationController)
        self.param_controller = self.app.controller(ParamController)

        self.dao = self.app.dao(CurrentDao)
        data = self.dao.load()
        self.bank_number = data["bank"]
        self.patch_number = data["patch"]

    # ************************
    # Property
    # ************************

    @property
    def current_patch(self):
        """
        Get the current :class:`Patch`
        """
        return self.current_bank.patches[self.patch_number]

    @property
    def current_bank(self):
        """
        Get the :class:`Bank` that contains the current :class:`Patch`
        """
        return self.banks_controller.banks[self.bank_number]

    # ************************
    # Persistance
    # ************************
    def _save_current(self):
        self.dao.save(self.bank_number, self.patch_number)

    # ************************
    # Get of Current
    # ************************
    def is_current_bank(self, bank):
        """
        :param Bank bank:
        :return bool: The :class:`Bank` is the current bank?
        """
        return bank == self.current_bank

    def is_current_patch(self, patch):
        """
        :param Patch patch:
        :return bool: The :class:`Patch` is the current patch?
        """
        return self.is_current_bank(patch.bank) and self.current_patch == patch

    # ************************
    # Set Current Patch/Bank
    # ************************
    def toBeforePatch(self, token=None):
        """
        Change the current :class:`Patch` for the previous patch.

        If the current patch is the first in the current :class:`Bank`,
        the current patch is will be the **last of the current Bank**.

        :param string token: Request token identifier
        """
        before_patch_number = self.patch_number - 1
        if before_patch_number == -1:
            before_patch_number = len(self.current_bank.patches) - 1

        self.set_patch(before_patch_number, token)

    def toNextPatch(self, token=None):
        """
        Change the current :class:`Patch` for the next patch.

        If the current patch is the last in the current :class:`Bank`,
        the current patch is will be the **first of the current Bank**

        :param string token: Request token identifier
        """
        next_patch_number = self.patch_number + 1
        if next_patch_number == len(self.current_bank.patches):
            next_patch_number = 0

        self.set_patch(next_patch_number, token)

    def set_patch(self, patch_number, token=None):
        """
        Set the current :class:`Patch` for the patch with
        ``index == patch_number`` only if the
        ``patch_number != currentPatch.index``

        :param int patch_number: Index of new current patch
        :param string token: Request token identifier
        """
        if self.patch_number == patch_number:
            return

        self._set_current(self.bank_number, patch_number, token=token)

    def toBeforeBank(self):
        """
        Change the current :class:`Bank` for the before bank. If the current
        bank is the first, the current bank is will be the last bank.

        The current patch will be the first of the new current bank.
        """
        banks = self.banks_controller.banks.all
        position = banks.index(self.current_bank)

        before = position - 1
        if before == -1:
            before = len(banks) - 1

        beforeBankIndex = banks[before].index

        self.set_bank(beforeBankIndex)

    def toNextBank(self):
        """
        Change the current :class:`Bank` for the next bank. If the current
        bank is the last, the current bank is will be the first bank.

        The current patch will be the first of the new current bank.
        """
        banks = self.banks_controller.banks.all
        position = banks.index(self.current_bank)

        nextBankIndex = position + 1
        if nextBankIndex == len(banks):
            nextBankIndex = 0

        nextBank = banks[nextBankIndex].index

        self.set_bank(nextBank)

    def set_bank(self, bank, token=None, notify=True):
        """
        Set the current :class:`Bank` for the bank
        only if the ``bank != current_bank``

        :param Bank bank: Bank that will be the current
        :param string token: Request token identifier
        :param bool notify: If false, not notify change for :class:`UpdatesObserver`
                            instances registered in :class:`Application`
        """
        if self.current_bank == bank:
            return

        self._set_current(bank, 0, token, notify)

    def _set_current(self, bank, patchNumber, token=None, notify=True):
        self._load_device_patch(  # throwable. need be first
            bank,
            patchNumber
        )
        self.bank_number = bank
        self.patch_number = patchNumber
        self._save_current()

        if notify:
            self.notifier.notifyCurrentPatchChange(self.current_patch, token)

    def _load_device_patch(self, bankNumber, patchNumber):
        bank = self.banks_controller.banks[bankNumber]
        patch = bank.patches[patchNumber]

        self.device_controller.loadPatch(patch)
