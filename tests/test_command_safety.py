from mcp_server.network_tools import is_safe_show_command


def test_allows_show_commands():
    assert is_safe_show_command("show version")
    assert is_safe_show_command("show interfaces status")
    assert is_safe_show_command("show ip bgp summary")


def test_blocks_config_commands():
    assert not is_safe_show_command("configure terminal")
    assert not is_safe_show_command("reload")
    assert not is_safe_show_command("copy running-config startup-config")
    assert not is_safe_show_command("delete flash:test")
    assert not is_safe_show_command("bash")


def test_blocks_show_with_dangerous_keywords():
    assert not is_safe_show_command("show running-config | include username")
    assert not is_safe_show_command("show tech | bash")
