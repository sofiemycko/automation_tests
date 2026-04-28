# Automation Tests

Tři automatizované testy pro web [engeto.cz](https://engeto.cz) napsané v Pythonu pomocí frameworku Playwright.

## Testované scénáře

1. **Katalog kurzů** - ověří, že stránka přehledu kurzů zobrazuje 3 neprázdné podkategorie se správnými názvy
2. **Kontaktní stránka** - ověří přítomnost nadpisu, e-mailového a telefonního odkazu
3. **Přihlašovací portál** - ověří, že zadání neplatných přihlašovacích údajů zobrazí chybovou hlášku

## Požadavky

- Python 3.8 nebo novější

## Instalace

```powershell
pip install -r requirements.txt
playwright install
```

## Spuštění testů

```powershell
pytest test_engeto.py
```

Spuštění s viditelným prohlížečem:

```powershell
pytest test_engeto.py --headed
```

Druhou možností je změnit `headless=False` v souboru `conftest.py`.
