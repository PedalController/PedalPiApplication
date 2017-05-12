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

from application.controller.component_data_controller import ComponentDataController

from test.controller.controller_test import ControllerTest


class ComponentDataControllerTest(ControllerTest):
    application = None
    controller = None
    banksController = None
    key = None

    def setUp(self):
        self.key = 'ComponentDataControllerTest'
        self.controller = self.get_controller(ComponentDataController)

    def get_controller(self, controller):
        return ComponentDataControllerTest.application.controller(controller)

    def test_empty_get(self):
        self.assertEqual(self.controller[self.key], {})

    def test_content_get(self):
        data = {'test': 'test_content_get'}

        self.controller[self.key] = data
        self.assertEqual(self.controller[self.key], data)

        del self.controller[self.key]

    def test_override_content(self):
        data = {'test': 'test_override_content'}
        data2 = {'test': 'test_override_content', 'fu': 'bá'}

        self.controller[self.key] = data
        self.assertEqual(self.controller[self.key], data)
        self.controller[self.key] = data2
        self.assertEqual(self.controller[self.key], data2)

        del self.controller[self.key]

    def test_directly_changes_not_works(self):
        self.controller[self.key] = {'test': 'test_directly_changes_not_works'}

        data = self.controller[self.key]
        data['new-key'] = 'new value'

        self.assertNotEqual(self.controller[self.key], data)

        del self.controller[self.key]

    def test_delete_content(self):
        data = {'test': 'test_delete_content'}

        self.controller[self.key] = data
        self.assertNotEqual(self.controller[self.key], {})
        del self.controller[self.key]

        self.assertEqual(self.controller[self.key], {})
