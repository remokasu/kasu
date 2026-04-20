"""JsonGenerator のユニットテスト（スキーマ直接検証 + jsonschema validate）"""
import json

import pytest

from generators.json_gen import JsonGenerator, SCHEMA_VERSION


SCHEMA_PATH = "tests/fixtures/kasu_output_schema.json"


@pytest.fixture
def schema():
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def target_files(tmp_path):
    f1 = tmp_path / "alpha.py"
    f1.write_text("def a():\n    return 1\n")
    f2 = tmp_path / "beta.md"
    f2.write_text("# Beta\n")

    return [
        {"path": str(f1), "size": f1.stat().st_size, "lines": 2},
        {"path": str(f2), "size": f2.stat().st_size, "lines": 1},
    ]


class TestJsonGeneratorSchema:
    def test_schema_version_is_fixed(self, tmp_path, target_files):
        gen = JsonGenerator()
        raw, _ = gen.generate(target_files, str(tmp_path))
        data = json.loads(raw)
        assert data["meta"]["schema_version"] == SCHEMA_VERSION == "1.0"

    def test_required_top_level_keys_present(self, tmp_path, target_files):
        gen = JsonGenerator()
        raw, _ = gen.generate(target_files, str(tmp_path))
        data = json.loads(raw)
        assert set(data.keys()) >= {"meta", "files"}

    def test_files_each_have_required_keys(self, tmp_path, target_files):
        gen = JsonGenerator()
        raw, _ = gen.generate(target_files, str(tmp_path))
        data = json.loads(raw)
        required = {
            "path", "absolute_path", "size", "lines", "tokens",
            "encoding", "language", "content", "truncated",
        }
        for f in data["files"]:
            assert required <= set(f.keys())

    def test_dry_run_sets_content_null_and_meta_flag(self, tmp_path, target_files):
        gen = JsonGenerator()
        raw, _ = gen.generate(
            target_files, str(tmp_path),
            render_context={"dry_run": True},
        )
        data = json.loads(raw)
        assert data["meta"]["dry_run"] is True
        for f in data["files"]:
            assert f["content"] is None

    def test_include_merge_false_sets_content_null(self, tmp_path, target_files):
        gen = JsonGenerator()
        raw, _ = gen.generate(target_files, str(tmp_path), include_merge=False)
        data = json.loads(raw)
        for f in data["files"]:
            assert f["content"] is None

    def test_default_mode_has_string_content(self, tmp_path, target_files):
        gen = JsonGenerator()
        raw, _ = gen.generate(target_files, str(tmp_path))
        data = json.loads(raw)
        for f in data["files"]:
            assert isinstance(f["content"], str)

    def test_truncate_flag_propagated_from_render_context(self, tmp_path, target_files):
        gen = JsonGenerator()
        raw, _ = gen.generate(
            target_files, str(tmp_path),
            render_context={"truncated": True, "truncate_reason": "max_bytes"},
        )
        data = json.loads(raw)
        assert data["meta"]["truncated"] is True
        assert data["meta"]["truncate_reason"] == "max_bytes"


class TestJsonGeneratorAgainstSchema:
    """jsonschema で Draft 2020-12 契約テスト"""

    def test_output_passes_schema_validation(self, tmp_path, target_files, schema):
        jsonschema = pytest.importorskip("jsonschema")

        gen = JsonGenerator()
        raw, _ = gen.generate(target_files, str(tmp_path))
        data = json.loads(raw)

        jsonschema.validate(instance=data, schema=schema)

    def test_dry_run_output_passes_schema_validation(
        self, tmp_path, target_files, schema
    ):
        jsonschema = pytest.importorskip("jsonschema")

        gen = JsonGenerator()
        raw, _ = gen.generate(
            target_files, str(tmp_path),
            render_context={"dry_run": True},
        )
        data = json.loads(raw)

        jsonschema.validate(instance=data, schema=schema)
