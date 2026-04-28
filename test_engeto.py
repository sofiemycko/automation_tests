import random
import string
from playwright.sync_api import Page, expect

###  Test 1: Katalog kurzů
# Stránka přehledu kurzů zobrazuje 3 neprazdne podkategorie
def test_katalog_kurzu(engeto_page: Page):
    # testovací data
    url = "https://engeto.cz/prehled-kurzu/"
    ocekavany_pocet_podkategorii = 3
    ocekavane_nazvy = {
        "Akademie na 3 měsíce",
        "Balíčky kurzů na 6 měsíců",
        "Krátkodobé kurzy na 1–4 dny",
    }

    # 1. přechod na stránku přehledu kurzů
    engeto_page.goto(url)

    # 2. ověření, že jsou zobrazeny všechny 3 podkategorie
    podkategorie = engeto_page.locator(".area-kurzy .menu-item-area").all()
    assert len(podkategorie) == ocekavany_pocet_podkategorii, (
        f"Očekávány {ocekavany_pocet_podkategorii} podkategorie, nalezeno {len(podkategorie)}."
    )

    # 3. každá podkategorie musí mít viditelný nadpis a alespoň jeden kurz
    for sekce in podkategorie:
        nazev = sekce.locator(".menu-item-area-title").inner_text().strip().replace("\xa0", " ")

        # ověření, že nadpis podkategorie existuje a má neprázdný text
        nadpis = sekce.locator(".menu-item-area-title")
        assert nadpis.count() == 1 and nazev != "", (
            f"Podkategorie nemá nadpis."
        )

        # ověření, že název podkategorie je jedním z očekávaných názvů
        assert nazev in ocekavane_nazvy, (
            f"Neočekávaný název podkategorie: '{nazev}'."
        )

        # ověření, že sekce obsahuje alespoň jeden kurz
        kurzy = sekce.locator(".menu-item").all()
        assert len(kurzy) >= 1, (
            f"Podkategorie '{nazev}' neobsahuje žádný kurz."
        )


###  Test 2: Kontaktní stránka
# Kontaktní stránka obsahuje správné kontaktní údaje
def test_kontaktni_stranka(engeto_page: Page):
    # testovací data
    url = "https://engeto.cz/kontakt/"
    ocekavany_nadpis = "Zeptej se, rádi odpovíme"
    ocekavany_email = "info@engeto.com"
    ocekavany_telefon = "+420 773 087 597"

    # 1. přechod na kontaktní stránku
    engeto_page.goto(url)

    # 2. ověření hlavního nadpisu
    heading = engeto_page.get_by_role("heading", name=ocekavany_nadpis)
    expect(heading).to_be_visible()

    # 3. ověření e-mailového odkazu
    email_link = engeto_page.get_by_role("link", name=ocekavany_email).first
    expect(email_link).to_be_visible()

    # 4. ověření telefonního odkazu
    phone_link = engeto_page.get_by_role("link", name=ocekavany_telefon).first
    expect(phone_link).to_be_visible()


###  Test 3: Přihlašovací stránka výukového portálu
# Přihlašovací formulář na neplatné údaje zobrazí správnou chybovou hlášku
def test_prihlaseni_portal(page: Page):
    # testovací data
    url = "https://portal.engeto.com/lobby/sign-in"
    neplatny_email = "neplatny." + "".join(random.choices(string.ascii_lowercase, k=5)) + "@gmail.com"
    neplatne_heslo = "SpatneHeslo123"

    # 1. přechod na přihlašovací stránku portálu
    page.goto(url)

    # 2. kliknutí na tlačítko pro přihlášení e-mailem a heslem
    page.get_by_role("button", name="Přihlásit se pomoci e-mailu a hesla").click()

    # 3. ověření, že se zobrazil formulář s polem e-mail a heslo
    email_field = page.get_by_role("textbox", name="E-mailová adresa")
    password_field = page.get_by_role("textbox", name="Heslo")
    expect(email_field).to_be_visible()
    expect(password_field).to_be_visible()

    # 4. vyplnění neplatných přihlašovacích údajů
    email_field.fill(neplatny_email)
    password_field.fill(neplatne_heslo)
    page.get_by_role("button", name="Pokračovat").click()

    # 5. ověření, že se zobrazila chybová hláška
    error_message = page.locator(".ulp-input-error-message").last
    expect(error_message).to_be_visible()
    expect(error_message).to_have_text("Nesprávný e-mail nebo heslo")
