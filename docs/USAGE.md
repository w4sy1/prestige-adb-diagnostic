# Użycie

Zainstaluj oficjalne Android SDK Platform Tools i dodaj adb do PATH. Włącz debugowanie
USB i zaakceptuj klucz komputera na własnym telefonie.
`python app.py --collect --output reports`
`python app.py --collect --device IDENTYFIKATOR --logcat-count`

Wybór urządzenia nie jest utrwalany w raporcie. Nie odczytujemy IMEI ani całego getprop.
Backendy Androida mogą być ograniczone przez wersję/OEM. Błędy modułów są jawne.
Logcat przechowuje tylko liczbę linii błędów, bez wiadomości mogących zawierać sekrety.
Permissions to lista dostępnych uprawnień; audyt uprawnień aplikacji należy do Android Inspector.
Uruchomienie ADB może uruchomić lokalny serwer ADB; nie zmienia ustawień telefonu.
