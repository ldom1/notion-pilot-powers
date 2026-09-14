"""Config leak / CRMSettings hygiene tests (D17)."""


from notion_pilot_powers.config import CRMSettings, load_settings


def test_env_file_not_read(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".env").write_text("NOTION_TOKEN=bogus\nOPENROUTER_API_KEY=x\n")
    for k in ("NOTION_TOKEN", "OPENROUTER_API_KEY", "PROSPER_MCP_URL"):
        monkeypatch.delenv(k, raising=False)
    s = load_settings()
    assert s.notion_token is None
    assert s.openrouter_api_key is None
    assert s.prosper_mcp_url is None


def test_blank_strings_become_none(monkeypatch):
    monkeypatch.setenv("PROSPER_MCP_URL", "   ")
    monkeypatch.setenv("OPENROUTER_API_KEY", "")
    s = CRMSettings()
    assert s.prosper_mcp_url is None
    assert s.openrouter_api_key is None


def test_no_localhost_prosper_default():
    s = CRMSettings()
    assert s.prosper_mcp_url is None
