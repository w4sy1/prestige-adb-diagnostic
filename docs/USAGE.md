# Użycie

Zainstaluj oficjalne Android SDK Platform Tools i dodaj adb do PATH. Włącz debugowanie
USB i zaakceptuj klucz komputera na własnym telefonie.
`python app.py --collect --output reports`
`python app.py --collect --device IDENTYFIKATOR --logcat-count`

Wybór urządzenia nie jest utrwalany w raporcie. Nie odczytujemy IMEI ani całego getprop.
Backendy Androida mogą być ograniczone przez wersję/OEM. Błędy modułów są jawne.
Logcat przechowuje agregaty błędów bez treści wiadomości.
Permissions to lista dostępnych uprawnień; audyt uprawnień aplikacji należy do Android Inspector.
Uruchomienie ADB może uruchomić lokalny serwer ADB; nie zmienia ustawień telefonu.

## Rozszerzenia 0.2.0

`--package-permissions com.example.app` odczytuje deklarowane i nadane uprawnienia
konkretnego pakietu (opcja powtarzalna). `--logcat-count` grupuje błędy E/F według tagu,
priorytetu i czasu, bez treści wiadomości. Raport zawiera dostępne właściwości SoC.
Nie jest to pełny audyt aktywnych ról/appops. Testy urządzeń Android/OEM pozostają wymagane.
