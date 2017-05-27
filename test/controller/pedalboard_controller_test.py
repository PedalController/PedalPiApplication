# Copyright 2017 SrMouraSilva
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest.mock import MagicMock, call

from application.controller.banks_controller import BanksController
from application.controller.current_controller import CurrentController
from application.controller.notification_controller import NotificationController
from application.controller.pedalboard_controller import PedalboardController, PedalboardError
from pluginsmanager.model.bank import Bank
from pluginsmanager.model.pedalboard import Pedalboard
from pluginsmanager.observer.update_type import UpdateType
from test.controller.controller_test import ControllerTest


class PedalboardControllerTest(ControllerTest):

    def setUp(self):
        self.TOKEN = 'PATCH_TOKEN'

        controller = PedalboardControllerTest.application.controller

        self.controller = controller(PedalboardController)
        self.current = controller(CurrentController)
        self.notifier = controller(NotificationController)

        self.manager = controller(BanksController).manager

    def test_created_pedalboard(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_created_pedalboard - bank')
        pedalboard = Pedalboard('test_created_pedalboard')
        pedalboard2 = Pedalboard('test_created_pedalboard2')

        bank.append(pedalboard)

        self.controller.created(pedalboard)
        observer.on_pedalboard_updated.assert_called_with(pedalboard, UpdateType.CREATED, token=None, index=0, origin=bank)

        bank.append(pedalboard2)
        self.controller.created(pedalboard2, self.TOKEN)
        observer.on_pedalboard_updated.assert_called_with(pedalboard2, UpdateType.CREATED, token=self.TOKEN, index=1, origin=bank)

        self.notifier.unregister(observer)

    def test_created_pedalboard_error(self):
        observer = MagicMock()
        self.notifier.register(observer)

        pedalboard = Pedalboard('test_created_pedalboard')

        with self.assertRaises(PedalboardError):
            self.controller.created(pedalboard)

        observer.on_pedalboard_updated.assert_not_called()

        self.notifier.unregister(observer)

    def test_updated_pedalboard(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_updated_pedalboard - bank')
        pedalboard = Pedalboard('test_updated_pedalboard')
        bank.append(pedalboard)

        pedalboard.name = 'test_updated_pedalboard2'
        self.controller.updated(pedalboard)

        observer.on_pedalboard_updated.assert_called_with(pedalboard, UpdateType.UPDATED, token=None, index=0, origin=bank)

        pedalboard.name = 'test_updated_pedalboard3'
        self.controller.updated(pedalboard, self.TOKEN)
        observer.on_pedalboard_updated.assert_called_with(pedalboard, UpdateType.UPDATED, token=self.TOKEN, index=0, origin=bank)

        self.notifier.unregister(observer)

    def test_updated_pedalboard_error(self):
        observer = MagicMock()
        self.notifier.register(observer)

        pedalboard = Pedalboard('test_updated_current_pedalboard')

        with self.assertRaises(PedalboardError):
            self.controller.updated(pedalboard)

        observer.on_pedalboard_updated.assert_not_called()

        self.notifier.unregister(observer)

    def test_updated_current_pedalboard(self):
        observer = MagicMock()
        self.notifier.register(observer)
        original_pedalboard = self.current.pedalboard

        bank = Bank('test_updated_current_pedalboard - bank')
        pedalboard = Pedalboard('test_updated_current_pedalboard')

        self.manager.append(bank)

        bank.append(pedalboard)
        self.controller.created(pedalboard)

        self.current.set_pedalboard(pedalboard)

        pedalboard.name = 'test_updated_current_pedalboard2'
        self.controller.updated(pedalboard)

        observer.on_pedalboard_updated.assert_called_with(pedalboard, UpdateType.UPDATED, token=None, index=0, origin=bank)

        self.assertEqual(self.current.pedalboard, pedalboard)
        self.assertEqual(self.current.bank, pedalboard.bank)

        pedalboard.name = 'test_updated_current_pedalboard3'
        self.controller.updated(pedalboard, self.TOKEN)
        observer.on_pedalboard_updated.assert_called_with(pedalboard, UpdateType.UPDATED, token=self.TOKEN, index=0, origin=bank)

        self.assertEqual(self.current.pedalboard, pedalboard)
        self.assertEqual(self.current.bank, pedalboard.bank)

        self.current.set_pedalboard(original_pedalboard)
        self.manager.banks.remove(bank)
        self.notifier.unregister(observer)

    def test_updated_current_pedalboard_set_all_data(self):
        """Not change only the pedalboard data, changes the pedalboard object"""
        observer = MagicMock()
        self.notifier.register(observer)
        original_pedalboard = self.current.pedalboard

        bank = Bank('test_updated_current_pedalboard_set_all_data - bank')
        pedalboard = Pedalboard('test_updated_current_pedalboard_set_all_data')

        self.manager.append(bank)

        bank.append(pedalboard)
        self.controller.created(pedalboard)

        self.current.set_pedalboard(pedalboard)

        new_pedalboard = Pedalboard('test_updated_current_pedalboard_set_all_data new pedalboard')
        bank.pedalboards[pedalboard.index] = new_pedalboard
        self.controller.updated(new_pedalboard)

        observer.on_pedalboard_updated.assert_called_with(new_pedalboard, UpdateType.UPDATED, token=None,
                                                          index=new_pedalboard.index, origin=bank)

        self.assertEqual(self.current.pedalboard, new_pedalboard)
        self.assertEqual(self.current.bank, new_pedalboard.bank)

        bank.pedalboards[new_pedalboard.index] = pedalboard
        self.controller.updated(pedalboard, self.TOKEN)
        observer.on_pedalboard_updated.assert_called_with(pedalboard, UpdateType.UPDATED, token=self.TOKEN,
                                                          index=pedalboard.index, origin=bank)

        self.assertEqual(self.current.pedalboard, pedalboard)
        self.assertEqual(self.current.bank, pedalboard.bank)

        self.current.set_pedalboard(original_pedalboard)
        self.manager.banks.remove(bank)
        self.notifier.unregister(observer)

    def test_deleted_pedalboard(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_deleted_pedalboard - bank')
        pedalboard = Pedalboard('test_deleted_pedalboard')
        pedalboard2 = Pedalboard('test_deleted_pedalboard2')

        bank.append(pedalboard)
        bank.append(pedalboard2)
        
        index = pedalboard.index
        bank.pedalboards.remove(pedalboard)

        self.controller.deleted(pedalboard, index, bank)
        observer.on_pedalboard_updated.assert_called_with(pedalboard, UpdateType.DELETED, token=None, index=index, origin=bank)

        index = pedalboard2.index
        bank.pedalboards.remove(pedalboard2)

        self.controller.deleted(pedalboard2, index, bank, self.TOKEN)
        observer.on_pedalboard_updated.assert_called_with(pedalboard2, UpdateType.DELETED, token=self.TOKEN, index=index, origin=bank)

        self.notifier.unregister(observer)

    def test_deleted_pedalboard_error(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_deleted_pedalboard_error - bank')
        pedalboard = Pedalboard('test_deleted_pedalboard')

        bank.append(pedalboard)
        with self.assertRaises(PedalboardError):
            self.controller.deleted(pedalboard, pedalboard.index, bank)

        observer.on_pedalboard_updated.assert_not_called()

        self.notifier.unregister(observer)

    def test_deleted_current_pedalboard(self):
        observer = MagicMock()
        self.notifier.register(observer)

        original_pedalboard = self.current.pedalboard

        bank = Bank('test_deleted_pedalboard - bank')
        pedalboard = Pedalboard('test_deleted_pedalboard')
        pedalboard2 = Pedalboard('test_deleted_pedalboard2')

        self.manager.append(bank)

        bank.append(pedalboard)
        bank.append(pedalboard2)

        self.controller.created(pedalboard)
        self.controller.created(pedalboard2)

        self.current.set_pedalboard(pedalboard)
        old_index = pedalboard.index
        bank.pedalboards.remove(pedalboard)
        self.controller.deleted(pedalboard, old_index=old_index, old_bank=bank)

        self.assertEqual(self.current.pedalboard, pedalboard2)
        self.assertEqual(self.current.bank, pedalboard2.bank)

        self.current.set_pedalboard(original_pedalboard)
        self.manager.banks.remove(bank)
        self.notifier.unregister(observer)

    def test_moved(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_moved - bank')

        bank.append(Pedalboard('Pedalboard 1'))
        bank.append(Pedalboard('Pedalboard 2'))
        bank.append(Pedalboard('Pedalboard 3'))
        bank.append(Pedalboard('Pedalboard 4'))

        pedalboard_moved = bank.pedalboards[-1]

        old_index = pedalboard_moved.index
        new_index = 1

        bank.pedalboards.move(pedalboard_moved, new_index)
        self.controller.moved(pedalboard_moved, old_index)

        expected = [
            call(pedalboard_moved, UpdateType.DELETED, index=old_index,
                 origin=bank, token=None),
            call(pedalboard_moved, UpdateType.CREATED, index=new_index,
                 origin=bank, token=None),
        ]

        self.assertListEqual(expected, observer.on_pedalboard_updated.call_args_list)

        # Token test
        observer.reset_mock()
        old_index = new_index
        new_index = 3

        bank.pedalboards.move(pedalboard_moved, new_index)
        self.controller.moved(pedalboard_moved, old_index, token=self.TOKEN)

        expected = [
            call(pedalboard_moved, UpdateType.DELETED, index=old_index,
                 origin=bank, token=self.TOKEN),
            call(pedalboard_moved, UpdateType.CREATED, index=new_index,
                 origin=bank, token=self.TOKEN)
        ]

        self.assertListEqual(expected, observer.on_pedalboard_updated.call_args_list)

        self.notifier.unregister(observer)

    def test_moved_current_pedalboard(self):
        original_current_pedalboard = self.current.pedalboard

        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_moved - bank')
        self.manager.append(bank)

        bank.append(Pedalboard('Pedalboard 1'))
        bank.append(Pedalboard('Pedalboard 2'))
        bank.append(Pedalboard('Pedalboard 3'))
        bank.append(Pedalboard('Pedalboard 4'))

        pedalboard_moved = bank.pedalboards[-1]
        new_index = 1

        self.current.set_pedalboard(pedalboard_moved)

        self.assertEqual(self.current.bank, bank)
        self.assertEqual(self.current.pedalboard, pedalboard_moved)

        self.controller.moved(pedalboard_moved, new_index)

        self.assertEqual(self.current.bank, bank)
        self.assertEqual(self.current.pedalboard, pedalboard_moved)

        self.current.set_pedalboard(original_current_pedalboard)
        self.manager.banks.remove(bank)
        self.notifier.unregister(observer)
