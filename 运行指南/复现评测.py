from pathlib import Path
import datetime, json, math, shutil, subprocess, sys

root = Path(__file__).resolve().parents[1]
run = root / '复现运行' / datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
evaluation = 'outputs/human-test180-20261026'
files = [f'{evaluation}/{n}' for n in ['evaluate_frozen.py', 'human_decisions_20261030.json', 'blind_sample.json']]
files += [f'outputs/feedback-baseline-20261026/{n}' for n in ['model.joblib', 'config.json', 'frozen_manifest.json']]
for name in files:
    target = run / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(root / name, target)
subprocess.run([sys.executable, str(run / evaluation / 'evaluate_frozen.py')], check=True)
actual_path = run / 'outputs/human-evaluation-20261030/metrics.json'
actual = json.loads(actual_path.read_text(encoding='utf-8'))
expected = json.loads((root / 'outputs/human-evaluation-20261030/metrics.json').read_text(encoding='utf-8'))
def compare(a, b, path):
    if isinstance(a, dict):
        assert a.keys() == b.keys(), path
        for key in a: compare(a[key], b[key], path + '/' + key)
    elif isinstance(a, float):
        assert math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-12), (path, a, b)
    else:
        assert a == b, (path, a, b)
for name in ['binary', 'always_negative_baseline', 'categories', 'category_micro', 'excluded_binary']:
    compare(expected[name], actual[name], name)
assert actual['verification']['model_hash_unchanged']
(run/'复现验证通过.txt').write_text('全部分类指标与已保存结果一致；冻结模型哈希通过；原项目结果未覆盖。\n', encoding='utf-8')
print('\nPASS: all metrics match the archived results.')
print('Output:', actual_path.parent)
