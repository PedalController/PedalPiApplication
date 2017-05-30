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

from pathlib import Path
from pluginsmanager.observer.autosaver.persistence import Persistence


class PluginsDao(object):
    """
    Persists and loads Lv2Plugins data
    """

    def __init__(self, data_path):
        """
        :param Path data_path:
        """
        self.data_path = data_path
        self.path = self.data_path / Path('plugins_lv2.json')

    def load(self):
        return Persistence.read(self.path)

    def save(self, data):
        Persistence.save(self.path, data)

    @property
    def exists_data(self):
        return self.path.exists()
