#!/usr/bin/env python3
"""Offline outside-scoring residual estimator; Python standard library only."""
import argparse
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path

D = Decimal
REFERENCE = json.loads((Path(__file__).resolve().parents[1] / 'references/calibration.json').read_text())
WEIGHTS = {'two': D(15), 'three': D(11), 'drive': D(22), 'offball': D(6)}

def number(value):
    result = D(str(value))
    if not result.is_finite() or result < 0:
        raise ValueError('Inputs must be finite and nonnegative')
    return result

def fmt(value):
    return str(value.quantize(D('0.000001')))

def level(value):
    if value < 76: return '偏低'
    if value < 110: return '中间水平'
    if value < 140: return '偏高'
    if value < 155: return '很高'
    return '极高'

def estimate(score, components, bonus_sum=None, components_exact=False, score_step='0.01'):
    e = number(score)
    step = number(score_step)
    if step == 0:
        raise ValueError('score_step must be positive')
    values = {key: number(components[key]) for key in WEIGHTS}
    error = sum((weight * (D(0) if components_exact else
                 D(1).scaleb(values[key].as_tuple().exponent))
                 for key, weight in WEIGHTS.items()), D(0))
    residual = 132 * e - sum((WEIGHTS[key] * value for key, value in values.items()), D(0))
    lower, upper = residual - error, residual + 132 * step
    result = {
        'inputs': {'score': str(score), **{k: str(v) for k,v in components.items()},
                   'bonus_sum': None if bonus_sum is None else str(bonus_sum)},
        'status': 'inconsistent' if upper < 0 else 'estimated',
        'effective': {'hidden_score_point': fmt(residual / 132),
                      'fadeaway_plus_pullup_point': fmt(residual),
                      'sum_envelope': None if upper < 0 else [fmt(max(D(0), lower)), fmt(upper)],
                      'hidden_score_envelope': None if upper < 0 else [fmt(max(D(0), lower)/132), fmt(upper/132)]},
        'interval_model': 'Conservative enclosure under downward truncation; upper boundary may be open. Not a statistical confidence interval.',
        'natural': None,
        'reference': REFERENCE,
    }
    if bonus_sum is not None:
        b = number(bonus_sum)
        low, high = lower-b, upper-b
        result['natural'] = {
            'status': 'inconsistent' if high < 0 else 'estimated',
            'hidden_score_point': fmt((residual-b)/132),
            'fadeaway_plus_pullup_point': fmt(residual-b),
            'sum_envelope': None if high < 0 else [fmt(max(D(0),low)),fmt(high)],
            'hidden_score_envelope': None if high < 0 else [fmt(max(D(0),low)/132),fmt(high/132)],
            'point_label': None if high < 0 or residual-b < 0 else level(residual-b),
            'envelope_labels': None if high < 0 else [level(max(D(0),low)),level(high)],
        }
    elif upper >= 0:
        result['comparison_if_no_related_bonus'] = {
            'point_label': None if residual < 0 else level(residual),
            'envelope_labels': [level(max(D(0),lower)),level(upper)],
            'note': 'Badge sum unknown; these labels are conditional, not an intrinsic rating.',
        }
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--score', required=True)
    for key in WEIGHTS: parser.add_argument('--'+key, required=True)
    parser.add_argument('--bonus-sum')
    parser.add_argument('--score-step', default='0.01')
    parser.add_argument('--components-exact', action='store_true')
    args = parser.parse_args()
    try:
        result = estimate(args.score, {key:getattr(args,key) for key in WEIGHTS},
                          args.bonus_sum, args.components_exact, args.score_step)
    except (InvalidOperation, ValueError, KeyError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__': main()
