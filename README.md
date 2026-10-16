# Oppgave 5 – Aktivitetsplanlegger

Arbeidskrav 1, Emne 1 (Gokstad Akademiet). Konsollprogram i Python for å planlegge og følge opp aktiviteter.

🇳🇴 [Norsk](#-norsk) · 🇬🇧 [English](#-english) · 🇹🇷 [Türkçe](#-türkçe)

---

# 🇳🇴 Norsk

## Funksjon
Programmet lar brukeren registrere aktiviteter med `title`, `category`, `date`, `estimated_minutes` og `status` (`planned` eller `completed`). Menyen vises på nytt etter hver handling til brukeren velger å avslutte.

Menyvalg:
1. Registrere og vise aktiviteter
2. Søke etter tittel eller kategori (store/små bokstaver spiller ingen rolle)
3. Filtrere etter status
4. Sortere etter dato (tidligst først) eller varighet (lengst først)
5. Markere en aktivitet som fullført
6. Vise antall aktiviteter, samlet estimert tid og antall fullførte
7. Lagre til fil og lese inn igjen
8. Avslutte programmet

## Bruk
Kjør fra mappen som inneholder filene:

~~~
python oppgave-5.py
~~~

Datoer skrives som `dd.mm.yyyy` (for eksempel `20.10.2026`). Varighet er et positivt heltall (minutter). Ved ugyldig input forklarer programmet feilen og spør på nytt, uten å stoppe.

Ved oppstart leses `activities.csv` automatisk. Finnes ikke filen, vises en melding og programmet fortsetter med en tom liste. Endringer blir bare lagret når brukeren velger 7 og `save`.

## Filstruktur
~~~
arbeidskrav-1-oppgave-5/
├── oppgave-5.py      programmet (klasse, funksjoner, meny)
├── activities.csv    eksempeldatafil (6 aktiviteter)
├── README.md         denne dokumentasjonen
└── .gitignore        utelater __pycache__/ og .idea/
~~~

Format på `activities.csv` (UTF-8, første linje er overskrift):

~~~
title,category,date,estimated_minutes,status
Read chapter 5,study,20.10.2026,45,planned
~~~

## Designvalg
- **Klassen `Activity`** samler dataene og handlingene som hører sammen: `describe()` gir en tekstlinje, `mark_completed()` setter status til `completed`, og `to_row()` gir en dictionary til CSV-filen. `__init__` er en initializer (slik det står i undervisningen). `status` har standardverdien `"planned"`, fordi en ny aktivitet alltid starter som planlagt. Arv er ikke brukt.
- **Datastruktur:** én `list` med `Activity`-objekter. Rekkefølgen de ble lagt inn i beholdes, siden `sorted()` returnerer en ny liste og ikke endrer originalen.
- **`date` lagres som `datetime.date`** i minnet (ikke som tekst), slik at sortering blir riktig. Tekstsortering ville sammenlignet dagen først. I filen og på skjermen vises datoen som `dd.mm.yyyy`.
- **Funksjoner** (utover klassemetodene): `get_valid_text`, `get_valid_date`, `get_positive_integer`, `get_valid_option`, `get_number_in_range`, `register_activity`, `show_activities`, `find_activities`, `filter_by_status`, `sort_activities`, `calculate_statistics`, `save_activities`, `load_activities`, `find_row_problem`, `show_menu`, `run_menu`. Funksjonene returnerer verdier, og utskriften gjøres av funksjonene som håndterer menyvalget.
- **Validering:** boolske flagg-variabler styrer løkkene (ikke `break`, `continue` eller `while True`). Dato må ha nøyaktig 10 tegn og være en gyldig dato (`31.02.2026` avvises). `strip()` fanger tekst som bare består av mellomrom. Kategorien lagres med små bokstaver, så søk og filter er konsekvente.
- **Fil:** `csv.DictWriter` og `csv.DictReader` med `encoding="utf-8"` og `newline=""`. Filsti med `Path(__file__).parent`. Manglende fil (`FileNotFoundError`) og manglende tilgang (`PermissionError`) håndteres med `try/except`. Rader med feil hoppes over med melding om linjenummer og årsak.
- **Utenfor pensum:** `csv`-modulen ([dokumentasjon](https://docs.python.org/3/library/csv.html)), `datetime` ([dokumentasjon](https://docs.python.org/3/library/datetime.html)) og `sorted(..., key=..., reverse=...)` (boka *Python Crash Course*) er ikke gjennomgått i slidene. Jeg valgte `csv` fremfor en egen tekstfilformat fordi `split` ikke er gjennomgått og en tittel kan inneholde skilletegn.

## Testtilfeller
| # | Hva testes | Input | Forventet resultat |
|---|---|---|---|
| 1 | Datafil mangler ved oppstart | start uten `activities.csv` | `No saved file found (activities.csv). Starting with an empty list.`, menyen vises |
| 2 | Ugyldig menyvalg | `x` | `Error: Invalid choice. Enter a number from 1 to 8.` |
| 3 | Ugyldig registrering | tom tittel, `31.02.2026`, varighet `abc`, `-5`, `0` | feilmelding for hver, spørsmålet gjentas, så `Registered: ...` |
| 4 | Søk | `STUDY` / `zzz` | `Read chapter 5` og `Practice Python` / `No activities match 'zzz'.` |
| 5 | Filter | `completed` (eksempelfilen) | `Evening walk` og `Grocery shopping` |
| 6 | Sortering | `date` / `duration` | dato: 17.10, 18.10, 19.10, 20.10, 21.10, 25.10 / varighet: 120, 90, 60, 45, 30, 10 |
| 7 | Fullføre og statistikk | fullfør `Read chapter 5`, velg 6 | `Number of activities: 6`, `Total estimated time: 355 min`, `Completed activities: 3` |
| 8 | Lagre og lese inn | velg 7: `save`, endre, `load` | `Saved ... to activities.csv.`, deretter opprinnelig tilstand tilbake |
| 9 | Skadet datafil | rader med tom tittel, `31.02.2026`, `abc`, `0`, `done` | `Skipped line N: ...` for hver, gyldige rader lastes |
| 10 | Feil overskrift | fil med kolonnene `a,b` | `Error: The file activities.csv does not have the expected columns: [...]` |

## Kjente feil og begrensninger
- Lagring overskriver filen uten advarsel, og det er ingen automatisk lagring ved avslutning. Ulagrede endringer går tapt.
- `load` erstatter den gjeldende listen. Leses en skadet fil, blir listen tom (og meldingen sier `Loaded 0 activities`).
- Aktiviteter kan ikke redigeres eller slettes, bare markeres som fullført.
- Datoer i fortiden er tillatt, og like titler er tillatt.
- `int()` godtar også former som `+45` som varighet.

## Forbedringsmuligheter
- Redigere og slette aktiviteter.
- Spørre om lagring ved avslutning, og lage sikkerhetskopi før overskriving.
- Spørre før `load` erstatter listen.
- Flere sorteringsretninger og filter på datoperiode.
- Automatiske tester (for eksempel `unittest`).

## Git-arbeidsflyt og historikk
Arbeidsflyt: opprettet et tomt repository på GitHub (`arbeidskrav-1-oppgave-5`), `git clone`, deretter for hvert delmål `git add`, `git commit -m "..."` og `git push`. README ble lagt til på slutten.

~~~
885e415 Add sample data file activities.csv
352ec99 Add sorting, completing, statistics and file saving
ca61fcd Add menu, input validation, register, search and filter
d08777d Add Activity class with describe and mark_completed
~~~

| Commit | Hva som ble gjort |
|---|---|
| `d08777d` | Første versjon: klassen `Activity` med `describe` og `mark_completed`, pluss `.gitignore` |
| `ca61fcd` | Hjelpefunksjoner for input med validering, menyen, registrering, søk og filter |
| `352ec99` | Sortering, markere som fullført, statistikk, lagring og innlesing (CSV), `to_row` |
| `885e415` | Eksempeldatafil `activities.csv` |
| (neste) | `README.md` |

---

# 🇬🇧 English

## What it does
A console program for planning and following up activities. Each activity has `title`, `category`, `date`, `estimated_minutes` and `status` (`planned` or `completed`). The menu is shown again after every action until the user quits.

Menu options: 1 register and show, 2 search title/category (case-insensitive), 3 filter by status, 4 sort by date (earliest first) or duration (longest first), 5 mark as completed, 6 statistics (count, total estimated time, completed), 7 save to file and read back, 8 quit.

## Usage
Run from the folder that contains the files:

~~~
python oppgave-5.py
~~~

Dates are typed as `dd.mm.yyyy`. Duration is a positive whole number (minutes). Invalid input is explained in the terminal and the user can try again; the program does not stop. At start-up `activities.csv` is read automatically. If it does not exist, a message is shown and the program continues with an empty list. Changes are only saved when the user chooses 7 and `save`.

## File structure
`oppgave-5.py` (program), `activities.csv` (sample data, 6 activities), `README.md`, `.gitignore`. The CSV file is UTF-8 with the header `title,category,date,estimated_minutes,status`.

## Design decisions
- **Class `Activity`** keeps data and actions together: `describe()`, `mark_completed()` and `to_row()`. `__init__` is an initializer. `status` defaults to `"planned"` because a new activity always starts as planned. No inheritance.
- **Data structure:** one `list` of `Activity` objects. `sorted()` returns a new list, so the insertion order is kept.
- **`date` is stored as `datetime.date`**, not text, so sorting is correct (text sorting would compare the day first). Shown and saved as `dd.mm.yyyy`.
- **Functions:** input functions with validation, `register_activity`, `show_activities`, `find_activities`, `filter_by_status`, `sort_activities`, `calculate_statistics`, `save_activities`, `load_activities`, `find_row_problem`, `show_menu`, `run_menu`. Functions return values, and the menu handlers do the printing.
- **Validation:** flag variables control the loops (no `break`, `continue` or `while True`). A date must be exactly 10 characters and a real date (`31.02.2026` is rejected). `strip()` catches spaces-only text. Categories are stored in lower case so search and filter are consistent.
- **File:** `csv.DictWriter` / `csv.DictReader` with `encoding="utf-8"` and `newline=""`, path from `Path(__file__).parent`. `FileNotFoundError` and `PermissionError` are handled with `try/except`. Invalid rows are skipped with the line number and the reason.
- **Outside the curriculum:** the `csv` module ([docs](https://docs.python.org/3/library/csv.html)), `datetime` ([docs](https://docs.python.org/3/library/datetime.html)) and `sorted(..., key=..., reverse=...)` (the book *Python Crash Course*) are not in the slides. I chose `csv` over my own text format because `split` is not in the slides and a title may contain the separator.

## Test cases
| # | What is tested | Input | Expected result |
|---|---|---|---|
| 1 | Data file missing at start | start without `activities.csv` | `No saved file found (activities.csv). Starting with an empty list.`, menu shown |
| 2 | Invalid menu choice | `x` | `Error: Invalid choice. Enter a number from 1 to 8.` |
| 3 | Invalid registration | empty title, `31.02.2026`, minutes `abc`, `-5`, `0` | an error message for each, the question is repeated, then `Registered: ...` |
| 4 | Search | `STUDY` / `zzz` | `Read chapter 5` and `Practice Python` / `No activities match 'zzz'.` |
| 5 | Filter | `completed` (sample file) | `Evening walk` and `Grocery shopping` |
| 6 | Sorting | `date` / `duration` | date: 17.10, 18.10, 19.10, 20.10, 21.10, 25.10 / duration: 120, 90, 60, 45, 30, 10 |
| 7 | Complete and statistics | complete `Read chapter 5`, choose 6 | `Number of activities: 6`, `Total estimated time: 355 min`, `Completed activities: 3` |
| 8 | Save and load | choose 7: `save`, change, `load` | `Saved ... to activities.csv.`, then the original state is back |
| 9 | Damaged data file | rows with empty title, `31.02.2026`, `abc`, `0`, `done` | `Skipped line N: ...` for each, valid rows are loaded |
| 10 | Wrong header | file with columns `a,b` | `Error: The file activities.csv does not have the expected columns: [...]` |

## Known issues
- Saving overwrites the file without a warning, and there is no automatic save on exit. Unsaved changes are lost.
- `load` replaces the current list. Reading a damaged file leaves an empty list (and the message says `Loaded 0 activities`).
- Activities cannot be edited or deleted, only marked as completed.
- Dates in the past and duplicate titles are allowed.
- `int()` also accepts forms like `+45` as duration.

## Ideas for improvement
Edit and delete; ask to save on exit and make a backup before overwriting; ask before `load` replaces the list; more sort directions and date-range filter; automated tests (for example `unittest`).

## Git workflow and history
Created an empty repository on GitHub (`arbeidskrav-1-oppgave-5`), `git clone`, then for each milestone `git add`, `git commit -m "..."` and `git push`. The README was added last.

| Commit | What was done |
|---|---|
| `d08777d` | First version: class `Activity` with `describe` and `mark_completed`, plus `.gitignore` |
| `ca61fcd` | Validated input functions, the menu, register, search and filter |
| `352ec99` | Sorting, mark as completed, statistics, save and load (CSV), `to_row` |
| `885e415` | Sample data file `activities.csv` |
| (next) | `README.md` |

---

# 🇹🇷 Türkçe

## İşlev
Aktiviteleri planlamak ve takip etmek için bir konsol programı. Her aktivitenin `title`, `category`, `date`, `estimated_minutes` ve `status` (`planned` veya `completed`) alanları var. Menü her işlemden sonra, kullanıcı çıkana kadar yeniden gösterilir.

Menü: 1 kaydet ve göster, 2 başlık/kategoriye göre ara (büyük-küçük harf fark etmez), 3 duruma göre filtrele, 4 tarihe (en erken önce) veya süreye (en uzun önce) göre sırala, 5 tamamlandı olarak işaretle, 6 istatistik (sayı, toplam tahmini süre, tamamlanan), 7 dosyaya kaydet ve geri oku, 8 çıkış.

## Kullanım
Dosyaların bulunduğu klasörden çalıştır:

~~~
python oppgave-5.py
~~~

Tarih `dd.mm.yyyy` biçiminde yazılır. Süre pozitif tam sayıdır (dakika). Geçersiz girişte hata terminalde açıklanır ve kullanıcı tekrar dener, program durmaz. Başlangıçta `activities.csv` otomatik okunur. Dosya yoksa mesaj gösterilir ve program boş bir listeyle devam eder. Değişiklikler yalnızca 7 ve `save` seçilince kaydedilir.

## Dosya yapısı
`oppgave-5.py` (program), `activities.csv` (örnek veri, 6 aktivite), `README.md`, `.gitignore`. CSV dosyası UTF-8'dir, başlık satırı `title,category,date,estimated_minutes,status`.

## Tasarım kararları
- **`Activity` sınıfı** veriyi ve işlemleri bir araya getirir: `describe()`, `mark_completed()` ve `to_row()`. `__init__` bir initializer'dır. `status` varsayılanı `"planned"`, çünkü yeni aktivite hep planlanmış başlar. Kalıtım kullanılmadı.
- **Veri yapısı:** `Activity` nesnelerinden oluşan tek bir `list`. `sorted()` yeni bir liste döndürür, bu yüzden ekleme sırası korunur.
- **`date` bellekte `datetime.date` olarak** saklanır (metin değil), böylece sıralama doğru olur (metin sıralaması önce günü karşılaştırırdı). Ekranda ve dosyada `dd.mm.yyyy` olarak görünür.
- **Fonksiyonlar:** doğrulamalı girdi fonksiyonları, `register_activity`, `show_activities`, `find_activities`, `filter_by_status`, `sort_activities`, `calculate_statistics`, `save_activities`, `load_activities`, `find_row_problem`, `show_menu`, `run_menu`. Fonksiyonlar değer döndürür, yazdırmayı menü işleyicileri yapar.
- **Doğrulama:** döngüleri bayrak değişkenleri yönetir (`break`, `continue`, `while True` yok). Tarih tam 10 karakter ve gerçek bir tarih olmalı (`31.02.2026` reddedilir). `strip()` yalnızca boşluktan oluşan metni yakalar. Kategori küçük harfle saklanır, böylece arama ve filtre tutarlı olur.
- **Dosya:** `csv.DictWriter` / `csv.DictReader`, `encoding="utf-8"` ve `newline=""`, yol `Path(__file__).parent` ile. `FileNotFoundError` ve `PermissionError` `try/except` ile yönetilir. Hatalı satırlar satır numarası ve nedenle atlanır.
- **Müfredat dışı:** `csv` modülü ([dokümantasyon](https://docs.python.org/3/library/csv.html)), `datetime` ([dokümantasyon](https://docs.python.org/3/library/datetime.html)) ve `sorted(..., key=..., reverse=...)` (*Python Crash Course* kitabı) slaytlarda yok. Kendi metin biçimim yerine `csv`'yi seçtim, çünkü `split` slaytlarda yok ve başlık ayırıcı karakter içerebilir.

## Test senaryoları
| # | Ne test edildi | Girdi | Beklenen sonuç |
|---|---|---|---|
| 1 | Başlangıçta veri dosyası yok | `activities.csv` olmadan başlat | `No saved file found (activities.csv). Starting with an empty list.`, menü görünür |
| 2 | Geçersiz menü seçimi | `x` | `Error: Invalid choice. Enter a number from 1 to 8.` |
| 3 | Geçersiz kayıt | boş başlık, `31.02.2026`, süre `abc`, `-5`, `0` | her biri için hata, soru tekrarlanır, sonra `Registered: ...` |
| 4 | Arama | `STUDY` / `zzz` | `Read chapter 5` ve `Practice Python` / `No activities match 'zzz'.` |
| 5 | Filtre | `completed` (örnek dosya) | `Evening walk` ve `Grocery shopping` |
| 6 | Sıralama | `date` / `duration` | tarih: 17.10, 18.10, 19.10, 20.10, 21.10, 25.10 / süre: 120, 90, 60, 45, 30, 10 |
| 7 | Tamamlama ve istatistik | `Read chapter 5` tamamla, 6 seç | `Number of activities: 6`, `Total estimated time: 355 min`, `Completed activities: 3` |
| 8 | Kaydet ve oku | 7 seç: `save`, değiştir, `load` | `Saved ... to activities.csv.`, sonra eski durum geri gelir |
| 9 | Bozuk veri dosyası | boş başlık, `31.02.2026`, `abc`, `0`, `done` içeren satırlar | her biri için `Skipped line N: ...`, geçerli satırlar yüklenir |
| 10 | Yanlış başlık | `a,b` sütunlu dosya | `Error: The file activities.csv does not have the expected columns: [...]` |

## Bilinen hatalar
- Kaydetme dosyanın üzerine uyarısız yazar, çıkışta otomatik kaydetme yoktur. Kaydedilmemiş değişiklikler kaybolur.
- `load` mevcut listeyi değiştirir. Bozuk bir dosya okunursa liste boş kalır (ve mesaj `Loaded 0 activities` der).
- Aktiviteler düzenlenemez veya silinemez, yalnızca tamamlandı olarak işaretlenir.
- Geçmiş tarihlere ve aynı başlıklara izin verilir.
- `int()` süre olarak `+45` gibi biçimleri de kabul eder.

## Geliştirme fikirleri
Düzenleme ve silme; çıkışta kaydetmeyi sorma ve üzerine yazmadan önce yedek alma; `load` listeyi değiştirmeden önce sorma; daha fazla sıralama yönü ve tarih aralığı filtresi; otomatik testler (örneğin `unittest`).

## Git iş akışı ve geçmiş
GitHub'da boş bir repository açıldı (`arbeidskrav-1-oppgave-5`), `git clone` yapıldı, sonra her aşamada `git add`, `git commit -m "..."` ve `git push`. README en sona eklendi.

| Commit | Ne yapıldı |
|---|---|
| `d08777d` | İlk sürüm: `Activity` sınıfı (`describe`, `mark_completed`) ve `.gitignore` |
| `ca61fcd` | Doğrulamalı girdi fonksiyonları, menü, kayıt, arama ve filtre |
| `352ec99` | Sıralama, tamamlama, istatistik, CSV'ye kaydetme ve okuma, `to_row` |
| `885e415` | Örnek veri dosyası `activities.csv` |
| (sonraki) | `README.md` |
