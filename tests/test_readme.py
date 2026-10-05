import os
import xml.etree.ElementTree as ET
import pytest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def test_files_exist():
    assert os.path.isfile(os.path.join(ROOT_DIR, "README.md")), "README.md not found"
    assert os.path.isfile(os.path.join(ROOT_DIR, "profile", "README.md")), "profile/README.md not found"
    assert os.path.isfile(os.path.join(ROOT_DIR, "assets", "banner.svg")), "assets/banner.svg not found"
    assert os.path.isfile(os.path.join(ROOT_DIR, "profile", "assets", "banner.svg")), "profile/assets/banner.svg not found"
    assert os.path.isfile(os.path.join(ROOT_DIR, "assets", "metrics.svg")), "assets/metrics.svg not found"
    assert os.path.isfile(os.path.join(ROOT_DIR, "profile", "assets", "metrics.svg")), "profile/assets/metrics.svg not found"

def test_svgs_valid():
    for svg_rel in [
        os.path.join("assets", "banner.svg"),
        os.path.join("profile", "assets", "banner.svg"),
        os.path.join("assets", "metrics.svg"),
        os.path.join("profile", "assets", "metrics.svg")
    ]:
        svg_path = os.path.join(ROOT_DIR, svg_rel)
        tree = ET.parse(svg_path)
        root = tree.getroot()
        assert root.tag.endswith("svg"), f"{svg_path} root tag is not svg"

@pytest.mark.parametrize("readme_path", [
    os.path.join(ROOT_DIR, "README.md"),
    os.path.join(ROOT_DIR, "profile", "README.md")
])
def test_readme_content(readme_path):
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert len(content) > 500, f"{readme_path} is too short"
    
    # Required Danton-org repositories and sections
    required_keywords = [
        "Danton.org",
        "Danton-org/DietIA",
        "Danton-org/CuiaHeads-Overpowered-Game",
        "Danton-org/.github",
        "BrunoDanton",
        "gbr-ufs",
        "everto-API",
        "DavissonC",
        "Métricas",
        "Projetos Oficiais",
        "Contribuidores",
        "Stack Tecnológica",
        "Como Contribuir",
    ]
    for kw in required_keywords:
        assert kw in content, f"Missing required keyword '{kw}' in {readme_path}"

    # Verify NO non-danton-org projects are listed
    prohibited_repos = [
        "Third-Person-Character-Controller-Package",
        "Psiculture-Management-Project",
        "TerrainProceduralGrassGenerator",
        "Garden-Wars",
        "CyberPong",
        "Desempacote"
    ]
    for non_org_repo in prohibited_repos:
        assert non_org_repo not in content, f"Non-Danton-org repo '{non_org_repo}' must not be present in {readme_path}"

def test_code_blocks_and_tables():
    for p in ["README.md", "profile/README.md"]:
        filepath = os.path.join(ROOT_DIR, p)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Check matching code block backticks
        assert content.count("```") % 2 == 0, f"Unbalanced code blocks in {p}"
