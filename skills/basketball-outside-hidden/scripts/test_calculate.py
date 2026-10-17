import unittest
from calculate import estimate

VALUES = {'two':'82', 'three':'71', 'drive':'65', 'offball':'83'}

class EstimatorTests(unittest.TestCase):
    def test_screenshot_badge_unknown(self):
        result = estimate('30.52', VALUES)
        self.assertEqual(result['effective']['fadeaway_plus_pullup_point'], '89.640000')
        self.assertEqual(result['effective']['hidden_score_point'], '0.679091')
        self.assertEqual(result['effective']['sum_envelope'], ['35.640000','90.960000'])
        self.assertIsNone(result['natural'])

    def test_known_badge_shift(self):
        result = estimate('30.52', VALUES, bonus_sum='23')['natural']
        self.assertEqual(result['fadeaway_plus_pullup_point'], '66.640000')
        self.assertEqual(result['sum_envelope'], ['12.640000','67.960000'])

    def test_exact_components_narrow_interval(self):
        result = estimate('30.52', VALUES, '0', components_exact=True)
        self.assertEqual(result['natural']['sum_envelope'], ['89.640000','90.960000'])

    def test_decimal_display_is_not_exact(self):
        values = {k:v+'.00' for k,v in VALUES.items()}
        result = estimate('30.52', values)
        self.assertEqual(result['effective']['sum_envelope'], ['89.100000','90.960000'])

    def test_incompatible_old_screenshot_not_low_rating(self):
        values = {'two':'65','three':'40','drive':'189','offball':'69'}
        result = estimate('20.00', values)
        self.assertEqual(result['status'], 'inconsistent')
        self.assertIsNone(result['effective']['sum_envelope'])
        self.assertNotIn('comparison_if_no_related_bonus',result)

    def test_threshold_spanning_interval(self):
        result = estimate('30.80', VALUES, '0')['natural']
        self.assertEqual(result['envelope_labels'], ['偏低','偏高'])

    def test_template_max_is_not_cap(self):
        result = estimate('32.00', VALUES, '0')['natural']
        self.assertGreater(float(result['sum_envelope'][0]),176)
        self.assertEqual(result['point_label'],'极高')

    def test_invalid_input(self):
        for score in ('NaN','Infinity','-1'):
            with self.assertRaises(ValueError): estimate(score,VALUES)
        with self.assertRaises(ValueError): estimate('30.52',VALUES,score_step='0')

if __name__ == '__main__': unittest.main()
