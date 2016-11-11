import unittest

from architecture.PatchError import PatchError

from model.Patch import Patch
from model.Effect import Effect


class PatchTest(unittest.TestCase):

    def _generate_patch(self, name):
        return {
            'name': name,
            'effects': [],
            'connections': []
        }

    def test_create_patch(self):
        json = self._generate_patch('generic-patch')

        patch = Patch(json)

        self.assertEqual(json, patch.json)

    def test_json(self):
        json = self._generate_patch('generic-patch')

        patch = Patch(json)

        self.assertEqual(json, patch.json)

    def test_set_json(self):
        """
        Show Patch.json (setter) for details of this test
        """
        json = self._generate_patch('generic-patch')
        json2 = self._generate_patch('generic-patch-2')

        patch = Patch(json)
        patch.json = json2

        self.assertEqual(json, patch.json)  # Show comment
        self.assertEqual(json2, patch.json)

    def test__getitem__(self):
        json = self._generate_patch('generic-patch')

        patch = Patch(json)

        self.assertEqual(patch.json['name'], patch['name'])

    def test__eq__(self):
        json = self._generate_patch('generic-patch')
        json2 = self._generate_patch('generic-patch')

        patch = Patch(json)
        patch2 = Patch(json2)

        self.assertEqual(patch, patch2)

    def test__ne__(self):
        json = self._generate_patch('generic-patch')
        json2 = self._generate_patch('generic-patch-2')

        patch = Patch(json)
        patch2 = Patch(json2)

        self.assertNotEqual(patch, patch2)

    def test_effects(self):
        json = self._generate_patch('generic-patch')
        json['effects'].append(self._generate_effect('Generic-EffectGxReverb-Stereo'))
        json['effects'].append(self._generate_effect('Generic-EffectGxReverb-Stereo2'))

        patch = Patch(json)

        effects = patch.effects
        for i in range(len(effects)):
            self.assertEqual(json['effects'][i], effects[i].json)

    def test_add_effect(self):
        json = self._generate_patch('generic-patch')

        patch = Patch(json)
        effect = Effect(self._generate_effect('Generic-EffectGxReverb-Stereo'))

        patch.addEffect(effect)

        self.assertEqual(effect, patch.effects[0])
        self.assertEqual(patch, effect.patch)

    def test_add_effect_added_in_other_patch(self):
        json = self._generate_patch('generic-patch')
        json2 = self._generate_patch('generic-patch2')

        patch = Patch(json)
        patch2 = Patch(json2)

        effect = Effect(self._generate_effect('Generic-EffectGxReverb-Stereo1'))
        patch.addEffect(effect)

        with self.assertRaises(PatchError):
            patch2.addEffect(effect)

    def test_delete_effect(self):
        json = self._generate_patch('generic-patch')

        patch = Patch(json)
        effect = Effect(self._generate_effect('Generic-EffectGxReverb-Stereo1'))

        total_effects = len(patch.effects)
        patch.addEffect(effect)

        index = effect.index
        self.assertEqual(patch.effects[index], effect)
        patch.deleteEffect(effect)

        with self.assertRaises(IndexError):
            patch.effects[index]

        self.assertEqual(len(patch.effects), total_effects)

    def test_delete_effect_of_other_patch(self):
        json = self._generate_patch('generic-patch')
        json2 = self._generate_patch('generic-patch2')

        patch = Patch(json)
        patch2 = Patch(json2)

        effect = Effect(self._generate_effect('Generic-EffectGxReverb-Stereo1'))
        patch.addEffect(effect)

        with self.assertRaises(PatchError):
            patch2.deleteEffect(effect)

    def test_index_of_effect(self):
        json = self._generate_patch('generic-patch')

        patch = Patch(json)

        patch.addEffect(Effect(self._generate_effect('Generic-EffectGxReverb-Stereo1')))
        patch.addEffect(Effect(self._generate_effect('Generic-EffectGxReverb-Stereo2')))
        patch.addEffect(Effect(self._generate_effect('Generic-EffectGxReverb-Stereo3')))
        patch.addEffect(Effect(self._generate_effect('Generic-EffectGxReverb-Stereo4')))

        index = 0
        for effect in patch.effects:
            self.assertEqual(index, effect.index)
            index += 1

    def _generate_effect(self, name):
        return {
            "name": name,
            "uri": "http://generic.efx",
            "author": {},
            "label": "Generic-EffectGxReverb-Stereo",
            "status": True,
            "ports": {
                "audio": {
                    "input": [{
                        "ranges": {},
                        "designation": "",
                        "index": 4,
                        "units": {},
                        "shortName": "in",
                        "properties": [],
                        "name": "in",
                        "symbol": "in",
                        "rangeSteps": None,
                        "scalePoints": []
                    }, {
                        "ranges": {},
                        "designation": "",
                        "index": 4,
                        "units": {},
                        "shortName": "in-right",
                        "properties": [],
                        "name": "in",
                        "symbol": "in-right",
                        "rangeSteps": None,
                        "scalePoints": []
                    }],
                    "output": [{
                        "symbol": "out",
                        "name": "Out",
                        "scalePoints": [],
                        "units": {},
                        "ranges": {},
                        "properties": [],
                        "rangeSteps": None,
                        "designation": "",
                        "index": 5,
                        "shortName": "Out"
                    }]
                },
                "midi": {
                    "input": [],
                    "output": []
                },
                "control": {
                    "input": [{
                        "symbol": "dry_wet",
                        "name": "Dry/Wet",
                        "scalePoints": [],
                        "value": 50,
                        "units": {},
                        "ranges": {
                            "minimum": 0,
                            "maximum": 100,
                            "default": 50
                        },
                        "properties": [],
                        "rangeSteps": None,
                        "designation": "",
                        "index": 0,
                        "shortName": "Dry/Wet"
                    }],
                    "output": []
                }
            }
        }

    def test_swap(self):
        json = self._generate_patch('generic-patch')
        effect1 = Effect(self._generate_effect('Generic-EffectGxReverb-Stereo1'))
        effect2 = Effect(self._generate_effect('Generic-EffectGxReverb-Stereo2'))

        patch = Patch(json)

        patch.addEffect(effect1)
        patch.addEffect(effect2)

        self.assertEqual(patch.effects, [effect1, effect2])
        patch.swapEffects(effect1, effect2)
        self.assertEqual(patch.effects, [effect2, effect1])

    def test_wrong_swap(self):
        json1 = self._generate_patch('generic-patch')
        json2 = self._generate_patch('generic-patch2')

        patch1 = Patch(json1)
        patch1.addEffect(Effect(self._generate_effect('Generic-EffectGxReverb-Stereo1')))
        patch1.addEffect(Effect(self._generate_effect('Generic-EffectGxReverb-Stereo2')))

        patch2 = Patch(json2)
        patch2.addEffect(Effect(self._generate_effect('Generic-EffectGxReverb-Stereo1')))
        patch2.addEffect(Effect(self._generate_effect('Generic-EffectGxReverb-Stereo2')))

        with self.assertRaises(PatchError):
            patch1.swapEffects(patch1.effects[0], patch2.effects[1])
