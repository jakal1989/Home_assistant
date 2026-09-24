import sys
import subprocess
import json
import re


def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])


install_and_import("requests")
install_and_import("bs4")

import requests
from bs4 import BeautifulSoup


def scrape():
    url = "https://www.bls.ch/de/unternehmen/projekte-und-hintergruende/bauprojekte/nachtarbeiten"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text(separator=" ", strip=True)

        # Mögliche Start-Anker (alte und neue Bezeichnung)
        possible_start_anchors = [
            "Bern–Köniz–Schwarzenburg",
            "Bern–Schwarzenburg",
        ]

        # Liste möglicher nächster Überschriften auf der BLS-Seite
        possible_end_anchors = [
            "Burgdorf–Langnau i.E. / Sumiswald-Grünen",
            "Langenthal–Wolhusen",
            "Langenthal–Huttwil–Wolhusen",
            "Moutier–Lengnau",
            "Solothurn–Moutier–Lengnau",
            "Solothurn–Burgdorf",
            "Solothurn–Moutier",
            "Spiez–Interlaken Ost",
            "Spiez–Kandersteg–Brig",
            "Spiez–Zweisimmen",
            "Thun–Konolfingen–Hasle-Rüegsau–Burgdorf",
            "Thun–Spiez",
            "Zusätzliche Nachtarbeiten",
        ]

        # Ersten passenden Start-Anker suchen
        start_anchor = None
        start_pos = -1

        for anchor in possible_start_anchors:
            pos = text.find(anchor)
            if pos != -1:
                start_anchor = anchor
                start_pos = pos
                break

        if start_pos != -1:
            # Frühesten End-Anker nach dem Start suchen
            end_pos = -1

            for anchor in possible_end_anchors:
                found_pos = text.find(anchor, start_pos + len(start_anchor))
                if found_pos != -1:
                    if end_pos == -1 or found_pos < end_pos:
                        end_pos = found_pos

            # Falls kein End-Anker gefunden wurde
            if end_pos == -1:
                content = text[
                    start_pos + len(start_anchor):
                    start_pos + len(start_anchor) + 500
                ].strip()
            else:
                content = text[
                    start_pos + len(start_anchor):end_pos
                ].strip()

            clean = re.sub(r"\s+", " ", content)

            # Falls praktisch kein Inhalt vorhanden ist
            if len(clean) < 10:
                print(json.dumps({
                    "status": "Ruhig",
                    "details": "Aktuell keine Details verfügbar."
                }))
            else:
                print(json.dumps({
                    "status": "Aktiv",
                    "details": clean[:500]
                }))
        else:
            print(json.dumps({
                "status": "Nicht gefunden",
                "details": "Keine Meldung verfügbar"
            }))

    except Exception as e:
        print(json.dumps({
            "status": "Fehler",
            "details": str(e)
        }))


if __name__ == "__main__":
    scrape()
