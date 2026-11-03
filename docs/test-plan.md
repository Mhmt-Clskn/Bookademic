# BookAcademic — Test Stratejisi ve Test Planı (Sprint 1)

| Doküman Özelliği | Değer |
| :--- | :--- |
| **Proje Adı** | BookAcademic |
| **Ders** | SENG 321 — Software Engineering Project |
| **Dosya** | `docs/test-plan.md` |
| **Sürüm** | v0.1.0-sprint1 |
| **Rol ve Sahip** | Mirac — Quality Assurance & Test Automation Engineer |
| **Danışılanlar** | Mürsel (mimari, M2), Mehmet (CI), Melih (kabul kriterleri) |
| **Hedef Modül** | M2 — Rezervasyon Çekirdeği (Ortak Motor); M1, M3, M4 entegrasyon ve E2E seviyesinde |
| **Test Kapsamı Hedefi** | Zorunlu: %50 satır kapsamı (Sprint 3 CI kapısı) · Hedef: %50 dal kapsamı, M2 için %80 satır |
| **İlgili Belgeler** | `docs/sprint1/backlog.md`, `docs/api/openapi.yaml`, `docs/adr/0001-tech-stack.md` |
| **Son Güncelleme** | 3 Kasım 2026 |

---

## 1. Amaç ve Kapsam

Bu doküman, BookAcademic sisteminin kalite güvence yaklaşımını, test piramidi dağılımını, birim (unit), entegrasyon (integration) ve uçtan uca (E2E) test gereksinimlerini belirler.

Sistem, öğrencinin proje geliştirme sürecinde ihtiyaç duyduğu iki temel kıt kaynağı (öğretim elemanının ofis saati ile laboratuvar cihazı ve odaları) tek bir ortak rezervasyon motoru (M2) üzerinde yönetir. Test stratejisinin ana hedefleri şunlardır:

1. **Sıfır Çift Rezervasyon:** Zaman aralığı kesişimlerinde çakışan taleplerin, eşzamanlı istekler dahil kesinlikle engellenmesi (`409 SLOT_UNAVAILABLE`).
2. **Sunucu Taraflı Yetki Denetimi:** Akademik onay (`LAB_APPROVAL_REQUIRED`) ve cihaz eğitim yetkisi (`TRAINING_REQUIRED`) bulunmayan taleplerin, arayüz atlanıp API doğrudan çağrılsa bile sunucu katmanında reddedilmesi (`403 Forbidden`).
3. **Sürdürülebilir Kalite Kapısı:** Sprint 3'te devreye girecek GitHub Actions hattında birim test kapsamının **%50 altına düşmemesi**.

**Kapsam dışı (Sprint 1–3):** Yük ve stres testi, güvenlik sızma testi, tarayıcı uyumluluk matrisi, mobil görünüm testi. Tek performans ölçütü US-12'deki katalog yanıt süresidir (bölüm 2.2).

---

## 2. Test Piramidi ve Test Seviyeleri

Sistem testleri piramit modeline uygun olarak üç ana katmanda koşturulacaktır:

```
          / \
         / E2E \        -> Demo Akışı & Kritik Yolculuk (Sprint 3 / Final)
        /-------\
       / Entegr. \      -> REST API + PostgreSQL + Mailpit (Sprint 2 / 3)
      /-----------\
     /  Birim/Unit \    -> M2 Çekirdek, Çakışma & Durum Makinesi (Sprint 1 / 2)
    /---------------\
```

Piramide ek olarak iki destek seviyesi vardır:

* **Sözleşme testleri:** Entegrasyon testlerinde API yanıtlarının `openapi.yaml`'daki şema ve durum kodlarına uyduğu doğrulanır. Geliştirme sırasında Prism mock sunucusu kullanılır.
* **Mimari testler:** ArchUnitNET ile M3 ve M4'ün M2'ye yalnızca `BookAcademic.Booking.Contracts` üzerinden eriştiği doğrulanır (sorumlu: Mürsel).

### 2.1 Birim Testler (Unit Tests)

* **Sorumlu:** QA Engineer (Mirac) & Modül Sahipleri
* **Kapsam:** M2 Rezervasyon Çekirdeği mantığı, zaman aralığı kesişim algoritmaları, durum geçişleri (state machine transition table), uygunluk politikaları ve girdi doğrulama kuralları. Veritabanı ve ağ kullanılmaz.
* **Test Çatısı ve Araçlar:**
  * Test Runner: `xUnit`
  * Mocking Kütüphanesi: `Moq`
  * Doğrulama (Assertion): xUnit `Assert` veya `Shouldly` (FluentAssertions, 8. sürümle ticari lisansa geçtiği için kullanılmaz; ADR 0001)
  * Kapsam Ölçümü: `coverlet.collector` (`dotnet test --collect:"XPlat Code Coverage"`)
* **Test Projesi:** `backend/tests/BookAcademic.Tests` (Sprint 1'de iskeleti kurulur, M2'ye referans verir)
* **Kapsam Hedefi:** Zorunlu **%50 satır kapsamı**; hedef **%50 dal kapsamı**. M2 için hedef %80 satır kapsamı.

> **Not:** Birim testler HTTP durum kodu değil, çekirdeğin döndürdüğü sonucu doğrular (ör. "çakışma var", `InvalidInterval`). Bu sonuçların `409`, `400` gibi HTTP yanıtlarına çevrilmesi bölüm 2.2'deki entegrasyon testlerinde doğrulanır. Tablolarda karşılık gelen HTTP yanıtı bilgi amaçlı verilmiştir.

#### 2.1.1 M2 Çakışma Motoru (US-06 / US-07)

Aralıklar yarı açıktır: `[başlangıç, bitiş)`.

| Test ID | Test Senaryosu | Girdi / Ön Koşul | Beklenen Sonuç (HTTP karşılığı) |
| :--- | :--- | :--- | :--- |
| `UT-CORE-01` | Tam Çakışan Aralık | Mevcut: 10:00-11:00, Talep: 10:00-11:00 | Çakışma (`409 SLOT_UNAVAILABLE`) |
| `UT-CORE-02` | Kısmi Kesişim (Başlangıç Örtüşmesi) | Mevcut: 10:00-11:00, Talep: 09:30-10:30 | Çakışma (`409`) |
| `UT-CORE-03` | Kısmi Kesişim (Bitiş Örtüşmesi) | Mevcut: 10:00-11:00, Talep: 10:30-11:30 | Çakışma (`409`) |
| `UT-CORE-04` | Kapsayan Aralık (İç İçe Talep) | Mevcut: 09:00-12:00, Talep: 10:00-11:00 | Çakışma (`409`) |
| `UT-CORE-05` | Uç Uca Dilim (Adjacent, sonra) | Mevcut: 10:00-11:00, Talep: 11:00-12:00 | Çakışma yok (`201`) |
| `UT-CORE-06` | Geçersiz Zaman Sıralaması | Başlangıç: 14:00, Bitiş: 13:00 | Geçersiz aralık (`400 INVALID_INTERVAL`) |
| `UT-CORE-07` | Sıfır Dakika Rezervasyon Sınırı | Başlangıç: 10:00, Bitiş: 10:00 | Geçersiz aralık (`400 INVALID_INTERVAL`) |
| `UT-CORE-08` | Uç Uca Dilim (Adjacent, önce) | Mevcut: 10:00-11:00, Talep: 09:00-10:00 | Çakışma yok (`201`) |
| `UT-CORE-09` | Talep Mevcudun İçinde | Mevcut: 10:00-11:00, Talep: 10:15-10:45 | Çakışma (`409`) |
| `UT-CORE-10` | Farklı Kaynak | Aynı aralık, başka cihaz | Çakışma yok (`201`) |
| `UT-CORE-11` | Pasif Durumdaki Kayıt | Mevcut kayıt `CANCELLED`, `REJECTED` veya `COMPLETED` | Çakışma yok (`201`) |
| `UT-CORE-12` | Aktif Durumdaki Kayıt | Mevcut kayıt `PENDING`, `APPROVED` veya `CHECKED_IN` | Çakışma (`409`) |

#### 2.1.2 Lab Erişim Kuralları (US-06 / US-13 / US-14)

Öğrenci "Osiloskop" kategorisindeki bir cihazı rezerve etmek istiyor.

| Test ID | Lab Onayı | Eğitim Yetkisi | Beklenen Sonuç (HTTP karşılığı) |
| :--- | :--- | :--- | :--- |
| `UT-ACCESS-01` | Yok | Yok | `403 LAB_APPROVAL_REQUIRED` |
| `UT-ACCESS-02` | Yok | Var | `403 LAB_APPROVAL_REQUIRED` |
| `UT-ACCESS-03` | Var | Yok | `403 TRAINING_REQUIRED` |
| `UT-ACCESS-04` | Var | Var | Uygun (`201`, durum `PENDING`) |
| `UT-ACCESS-05` | Süresi dolmuş | Var | `403 LAB_APPROVAL_REQUIRED` (bkz. bölüm 11) |
| `UT-ACCESS-06` | Başka kategori (FPGA) | Var | `403 LAB_APPROVAL_REQUIRED` |
| `UT-ACCESS-07` | Var | Başka kategori (FPGA) | `403 TRAINING_REQUIRED` |
| `UT-ACCESS-08` | Var | Var, cihaz bakımda | `409 RESOURCE_IN_MAINTENANCE` |

#### 2.1.3 Durum Makinesi (US-08 / US-09)

| Test ID | Geçiş | Beklenen Sonuç (HTTP karşılığı) |
| :--- | :--- | :--- |
| `UT-STATE-01` | `PENDING` → onayla | `APPROVED`; durum geçmişine kayıt |
| `UT-STATE-02` | `PENDING` → reddet (gerekçeli) | `REJECTED`; gerekçe geçmişte |
| `UT-STATE-03` | Reddet, gerekçe boş veya 5 karakterden kısa | Doğrulama hatası (`400`) |
| `UT-STATE-04` | `APPROVED`, `REJECTED` veya `CANCELLED` kaydı onayla | Geçersiz geçiş (`409 INVALID_STATE_TRANSITION`) |
| `UT-STATE-05` | Sahibi başlangıçtan önce iptal eder | `CANCELLED`; aralık yeniden rezerve edilebilir |
| `UT-STATE-06` | Başlangıç zamanı geçmiş kaydı iptal | `409 CANCELLATION_WINDOW_PASSED` |

---

### 2.2 Entegrasyon Testleri (Integration Tests)

* **Kapsam:** REST API Controller katmanı, yetkilendirme (`401`/`403`), PostgreSQL veritabanı sorguları ve kısıtları, dış servis izolasyonu.
* **Araçlar:** xUnit, `WebApplicationFactory`, Testcontainers (PostgreSQL 17). Her test çalıştırması temiz bir veritabanıyla başlar.
* **Test Projesi:** `backend/tests/BookAcademic.IntegrationTests` (Sprint 2'de kurulur)
* **Mock Yaklaşımı:** Dış bağımlılık olan SMTP servisi geliştirme ve CI ortamında `Mailpit` konteyneri ile simüle edilir.
* **Kritik Test Senaryoları:**
  1. **Yarış Durumu Testi (Concurrency Test):** Aynı kaynağa ve aralığa eşzamanlı gelen iki talepte yalnızca birinin `201 Created`, diğerinin `409 SLOT_UNAVAILABLE` alması ve veritabanında tek kayıt bulunması. Bu test PostgreSQL'deki `EXCLUDE` kısıtını doğrular; bu yüzden gerçek veritabanıyla çalışmak zorundadır. Aynı test ofis saati slotu için de (US-18) tekrarlanır.
  2. **Lab Onay Akışı (US-13):** Hoca kendi ofis saati randevusundan lab onayı verdiğinde (`POST /api/v1/lab-approvals`) kaydın `active: true` olarak yazılması ve Arş. Gör.'ün `GET /api/v1/lab-approvals` ile listeleyebilmesi. Öğrenci veya Arş. Gör. onay vermeye çalışırsa `403`.
  3. **Sekreter Toplu İptali ve Hata İzolasyonu (US-20):** Sekreter bir ofis saatini belirli bir gün için iptal ettiğinde (`POST /api/v1/office-hours/{scheduleId}/cancellations`) o güne ait tüm randevuların `CANCELLED` statüsüne geçmesi. Mailpit servisine ulaşılamasa dahi veritabanındaki iptal işleminin güvenle tamamlanması (hata izolasyonu).
  4. **Kontrol Sırası (US-06):** Birden fazla kural ihlal edildiğinde OpenAPI'deki sıranın izlenmesi: kimlik (`401`) → aralık (`400`) → kaynak (`404`) → bakım (`409`) → lab onayı (`403`) → eğitim yetkisi (`403`) → çakışma (`409`).
  5. **Kimlik ve Rol (US-01 / US-02):** Okul dışı e-posta `400 EMAIL_DOMAIN_NOT_ALLOWED`; kayıtlı e-posta `409`; hatalı parola `401`; token olmadan korumalı uç nokta `401`; yetkisiz rol (ör. öğrencinin onay vermesi) `403`.
  6. **Eğitim Yetkisi (US-14):** TRAINING randevusu tamamlanınca yetki oluşur; OFFICE_HOUR randevusuyla denenirse `400 NOT_A_TRAINING_APPOINTMENT`; aynı kategori için ikinci yetki `409 TRAINING_ALREADY_GRANTED`.
  7. **Ofis Saati Tanımı (US-17):** 14:00–16:00 aralığı ve 30 dakikalık slotla 4 slot üretilmesi; TRAINING türünde kategori yoksa `400`; aynı kişinin çakışan iki saat tanımı `409 SCHEDULE_OVERLAP`.
  8. **Performans Eşiği (US-12):** 500 sentetik cihaz/oda kaydı içeren veritabanında katalog listeleme (`GET /api/v1/resources`) p95 yanıt süresinin **200 ms altında** kaldığının, 50 ardışık istekle doğrulanması.

---

### 2.3 Uçtan Uca (E2E) Testler ve MVP Demo Akışı (Golden Path)

* **Araç:** Playwright (Sprint 3'ten itibaren)

Sprint 3 MVP ve Hafta 10 Jüri demosu için sistem omurgasını oluşturan kritik yolculuk uçtan uca doğrulanacaktır:

```
[1. Hoca Slot Tanımlar (US-17)]
       ↓
[2. Öğrenci Konu Notuyla Randevu Alır (US-18)]
       ↓
[3. Hoca Görüşmeden Lab Onayı Verir (US-13)]
       ↓
[4. Öğrenci Cihaz Eğitimini Tamamlar ve Yetkilendirilir (US-14)]
       ↓
[5. Yetkili Öğrenci Lab Cihazı Rezerve Eder (US-06)]
       ↓
[6. Arş. Gör. Talebi Onaylar (US-08)]
```

Ek E2E senaryoları:

* **E2E-02 (Olumsuz Yol):** Onayı olmayan öğrenci rezervasyon dener; arayüz "lab erişim onayı gerekiyor" mesajını ve randevu ekranına bağlantıyı gösterir.
* **E2E-03 (Sekreter İptali):** Sekreter bir ofis saatini iptal eder; öğrencinin takviminde randevu iptal olarak görünür.

---

## 3. Sınır Değer Analizi (BVA) ve Kabul Kriterleri Doğrulaması

* **US-06 (Lab Rezervasyonu):** Bitiş $\le$ Başlangıç -> `400 INVALID_INTERVAL`. Kontrol sırası bölüm 2.2 madde 4'teki gibidir.
* **US-18 (Konu Notlu Randevu):** `10 - 500 karakter` aralığı için sınır testleri (baştaki ve sondaki boşluklar kırpılarak sayılır):
  * 9 karakter: `400 Bad Request`
  * 10 karakter: `201 Created`
  * 500 karakter: `201 Created`
  * 501 karakter: `400 Bad Request`
  * Salt boşluk karakterleri (whitespace): `400 Bad Request`
  * Aynı hocadan aynı gün ikinci randevu: `409 DAILY_APPOINTMENT_LIMIT`
  * Farklı hocalardan aynı gün iki randevu: `201 Created`
* **US-20 (Sekreter Ofis Saati İptali):** Yalnızca `SECRETARY`, `ADMIN` rolü veya saatin sahibi yetkilidir (aksi `403`). İptal gerekçesi en az 5 karakter olmalıdır (aksi `400`).

---

## 4. Hata Yönetimi ve Takip (Defect Tracking)

* Tespit edilen tüm işlevsel ve mantıksal hatalar GitHub Issues üzerinde **`bug`** etiketi ve ilgili modül etiketiyle (`M1-identity`, `M2-core`, `M3-lab`, `M4-office-hours`) açılır.
* Hata bildirimlerinde bulunması zorunlu alanlar:
  1. **Ortam (Environment):** Docker, Local OS, DB sürümü.
  2. **Yeniden Oluşturma Adımları (Steps to Reproduce):** İstek gövdesi (payload) ve HTTP metodu.
  3. **Beklenen Sonuç (Expected Result):** HTTP durum kodu ve dönmesi gereken şema.
  4. **Gerçekleşen Sonuç (Actual Result):** Alınan hata kodu, response gövdesi veya log kaydı.
  5. **İlgili Story:** Ör. US-06.
  6. **Önem Seviyesi (Severity):**

| Seviye | Tanım | Örnek | Hedef Çözüm |
| :--- | :--- | :--- | :--- |
| Blocker | Ana yolculuk veya veri bütünlüğü bozulur | Çift rezervasyon oluşur | Aynı gün |
| Major | Bir Must story çalışmaz | Lab onayı kaydedilmiyor | Sprint içinde |
| Minor | Should story, ikincil akış, görsel veya metin hatası | Yanlış Türkçe mesaj | Sonraki sprint |

* Her hata düzeltmesi, hatayı yeniden üreten bir testle birlikte gelir (regresyon testi).

---

## 5. Kalite Kapıları (Quality Gates - CI/CD)

```
[Pull Request Açılışı]
       ↓
[Build & Derleme]
       ↓
[xUnit Birim + Entegrasyon Testleri]
       ↓
[Kapsam Ölçümü (coverlet)]
       ↓
[Eşik Kontrolü: Satır Kapsamı >= %50]
       ├── GEÇTİ -> PR İncelemeye Açılır (Mirac / Mürsel Review)
       └── KALDI -> PR Birleştirmesi Engellenir (Merge Blocked)
```

1. **Eşik Kontrolü:** `coverlet.collector` kapsamı ölçer ancak düşük kapsamda testi başarısız saymaz. CI'daki eşik, EN-04 kapsamında `coverlet.msbuild` (`/p:Threshold=50`) veya ReportGenerator ile uygulanır (sorumlu: Mehmet). Otomatik üretilen kod (EF Core migration'ları, `Program.cs`) kapsam hesabının dışında tutulur.
2. **Commit Standardı:** Conventional Commits kuralına uygun olarak `test(M2): add overlap conflict unit tests (#12)` şeklinde yazılmalıdır.
3. **Branch Koruması:** `develop` ve `main` dallarına doğrudan push yapılamaz; en az 1 PR onayı ve (Sprint 3'ten itibaren) testlerin başarıyla geçmesi zorunludur.
4. **Statik Analiz:** Sprint 3 ve final tesliminde SonarQube analizi çalıştırılarak teknik borç QA tarafından raporlanacaktır.

---

## 6. Test Ortamı ve Test Verisi

* **Yerel:** `docker compose up` ile `db`, `api`, `web` ve `mailpit`. Gönderilen e-postalar Mailpit arayüzünde kontrol edilir.
* **CI:** GitHub Actions; entegrasyon testleri Testcontainers ile her çalıştırmada temiz bir PostgreSQL açar.
* **Test Verisi:** Yalnızca sentetik veri kullanılır, gerçek öğrenci verisi kullanılmaz (KVKK). Her rol için en az bir kullanıcı, iki cihaz kategorisi (Osiloskop, FPGA), her kategoride iki cihaz, bir oda, bir hoca ofis saati ve bir eğitim saati içeren tekrar üretilebilir bir tohum veri (seed) betiği hazırlanır.
* **Zaman:** Tüm test zamanları açık ofsetle yazılır (`+03:00`). "Şimdi"ye bağlı kurallar (ör. başlangıçtan önce iptal) için sistem saati `TimeProvider` üzerinden alınır ve testlerde sabitlenir.

---

## 7. Giriş ve Çıkış Ölçütleri

**Giriş (story teste hazır):** Kabul kriterleri test edilebilir biçimdedir (bölüm 8), ilgili OpenAPI operasyonu tanımlıdır ve bağımlı story'ler `develop`'a birleşmiştir.

**Çıkış (story tamam, Definition of Done ile uyumlu):**

* Her kabul kriteri en az bir otomatik testle karşılanır.
* Testler CI'da geçer; kapsam eşiğinin altına düşülmez.
* Yanıtlar OpenAPI sözleşmesiyle uyumludur.
* PR en az bir kişi tarafından onaylanmıştır; kod PR'larında onay Mürsel veya Mirac'tandır.

**Sprint sonu:** Açık Blocker hata yoktur; ana yolculuk demo provasında baştan sona çalışır.

---

## 8. Kabul Kriterlerinin Test Edilebilirlik İncelemesi

Aşağıdaki maddeler ilgili issue'lara yorum olarak yazılacak ve story sahibiyle netleştirilecektir. Netleşen yanıt hem issue'ya hem bu tabloya işlenir.

| Story | Belirsizlik | Önerilen Netleştirme |
| :--- | :--- | :--- |
| US-01 | "Okul uzantılı e-posta" hangi alan adları? | İzin verilen alan adları yapılandırma dosyasında listelenir. |
| US-06 | Geçmiş bir zamana rezervasyon yapılabilir mi? Azami süre var mı? | Geçmiş zaman `400`; azami süre (ör. 4 saat) Melih ile kararlaştırılır. |
| US-06 | Kriter yalnızca "bekleyen/onaylı" kayıtlarla çakışmayı yazıyor; `CHECKED_IN` kayıt da çakışmalı. | Kritere `CHECKED_IN` eklenir. |
| US-08 | Ret gerekçesinin asgari uzunluğu? | OpenAPI'deki gibi en az 5 karakter. |
| US-09 | Tam başlangıç anında iptal edilebilir mi? | Başlangıç anı dahil değildir (başlangıç ≤ şimdi → `409`). |
| US-12 | "200 ms" hangi veri boyutu ve ölçütle? | 500 kaynak, p95, CI ortamı (bölüm 2.2 madde 8). |
| US-13 | Bitiş tarihi geçmiş veya bugün olabilir mi? Onay hangi ana kadar geçerli? | Bitiş tarihi bugünden sonra olmalı; onay bitiş günü sonuna kadar geçerli. |
| US-14 | "Dönem boyunca geçerli": dönem sonu nereden bilinir? Hoca bildirimi Should olan US-04'e bağlı. | Dönem sonu yapılandırmadan gelir. Bildirim mekanizması netleşene kadar "bildirim kaydı oluştu" doğrulanır. |
| US-17 | Saat aralığı slot süresine tam bölünmezse (14:00–16:00, 45 dk)? Hangi rol hangi türü tanımlar? | Artan süre slot üretmez. Hoca OFFICE_HOUR, Arş. Gör. SUPPORT ve TRAINING tanımlar. |
| US-18 | Konu notu boşluk içeriyorsa nasıl sayılır? | Baştaki ve sondaki boşluklar kırpılarak sayılır; yalnızca boşluk `400`. |
| US-20 | Geçmiş bir gün veya zaten iptal edilmiş bir gün iptal edilebilir mi? | Geçmiş gün `400`; zaten iptal edilmiş gün tekrar iptalde etkilenen sayı 0 döner. |
| US-15 | Teslim kodunun geçerlilik süresi? | Rezervasyon başlangıcından 30 dk öncesi ile bitişi arası (Melih onayı). |
| US-16 | Bakıma alınan cihaz o anda `CHECKED_IN` ise? | Etkin kullanım bitene kadar bakım başlatılamaz (`409`); karar Sıla ile. |

---

## 9. Sprint Takvimi

| Sprint | Test İşleri |
| :--- | :--- |
| Sprint 1 (5 Kasım) | Bu plan; kabul kriteri incelemesi ve issue yorumları; `BookAcademic.Tests` iskeleti ve ilk örnek test (aralık çakışma kuralı) |
| Sprint 2 (5. hafta) | Fonksiyonel olmayan gereksinim ölçütleri; seed betiği; entegrasyon test projesi iskeleti |
| Sprint 3 (8. hafta) | M2 birim testleri (bölüm 2.1); eşzamanlılık testleri; CI'da %50 eşiği; E2E Golden Path |
| Final (10. hafta) | Tüm E2E senaryoları; entegrasyon ve E2E test raporu; SonarQube raporuyla birlikte kapsam raporu |

---

## 10. Riskler

| Risk | Önlem |
| :--- | :--- |
| Kapsamın %50'nin altında kalması | M2 testleri kodla birlikte yazılır; CI eşiği Sprint 3'te devreye girer; PR'da kapsam düşüşü review'da sorulur |
| Entegrasyon testlerinin yavaşlaması | Birim ve entegrasyon testleri ayrı projelerde; PostgreSQL konteyneri test sınıfları arasında paylaşılır |
| Zamana bağlı testlerin kararsızlığı | `TimeProvider` ile sabit saat; tüm zamanlar açık ofsetle |
| Bildirim kriterlerinin test edilememesi | Bildirim mekanizması netleşene kadar "bildirim kaydı oluştu" doğrulanır; e-posta Mailpit ile kontrol edilir |
| Frontend'in test dışında kalması | Ana yolculuk E2E ile korunur; frontend birim testleri açık nokta (bölüm 11) |

---

## 11. Açık Noktalar

* **Süresi dolmuş lab onayı hata kodu:** OpenAPI şu an süresi dolmuş onay için de `LAB_APPROVAL_REQUIRED` döndürüyor. Öğrenciye daha açıklayıcı mesaj göstermek için ayrı bir `LAB_APPROVAL_EXPIRED` kodu önerilir; Mürsel sözleşmeye eklerse `UT-ACCESS-05` güncellenir.
* **Test projesi adı:** `BookAcademic.Tests` veya `BookAcademic.Booking.UnitTests` (Mürsel ile).
* **Frontend testleri:** %50 kapsam yalnızca backend için mi ölçülecek? Bütün repo için ölçülecekse Vitest ve React Testing Library eklenir.
* **US-14 uç noktası:** `POST /training-authorizations` mı, `POST /appointments/{id}/complete` mı (Melih ile)? Karar sonrası bölüm 2.2 madde 6 güncellenir.
* **Bildirim önceliği:** US-04 Must'a çekilirse US-14 ve US-20'deki bildirim kriterleri doğrudan test edilir.
