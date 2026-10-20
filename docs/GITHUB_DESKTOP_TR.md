# GitHub Desktop ile projeyi GitHub'a yükleme (Windows)

Bu kılavuz, projelerini **`D:\GitHub`** altında saklayan kullanıcılar için hazırlanmıştır. Projenin doğrudan GitHub Desktop ile yönetilmesi hedeflenir; komut satırı veya `git init` kullanmak zorunda değilsin.

## 1. ZIP'i doğru konuma çıkar

1. Proje ZIP dosyasını indir.
2. İçindeki **`ee3005-image-processing-assignment-2`** klasörünü `D:\GitHub` içine çıkart.
3. Aşağıdaki dosyanın varlığını kontrol et:

   `D:\GitHub\ee3005-image-processing-assignment-2\README.md`

   **Yanlış:** `D:\GitHub\ee3005-image-processing-assignment-2\ee3005-image-processing-assignment-2\README.md`

4. Proje içeriğini **ZIP'ten çıkardıktan sonra** GitHub Desktop'a ekle; ZIP'i doğrudan repo dosyası olarak yükleme.

## 2. GitHub Desktop'ta yerel repository oluştur

1. **GitHub Desktop → File → Add local repository...** menüsünü aç.
2. **Choose...** ile `D:\GitHub\ee3005-image-processing-assignment-2` klasörünü seç.
3. Klasör henüz bir Git repository değilse GitHub Desktop'ın sunduğu **Create a repository here** seçeneğini kullan.
4. Repository adını `ee3005-image-processing-assignment-2` olarak ayarla ve işlemi tamamla.

**Not:** GitHub Desktop sürümüne bağlı olarak bu uyarı/ekran farklı görünebilir. Mevcut klasörde repo oluşturmayı önermiyorsa **File → New repository...** menüsünden repository name `ee3005-image-processing-assignment-2` ve **Local path** `D:\GitHub` seç. Oluşturulan repo klasörünün içine projedeki dosyaları (README, MATLAB, Report vb.) kopyala; iç içe ikinci proje klasörü oluşturma.

## 3. İlk commit

1. Sol taraftaki **Changes** bölümünden eklenecek dosyaları kontrol et.
2. `.gitignore`, `README.md`, `MATLAB/`, `Python_Reference/`, `Source_Images/`, `Report/`, `Outputs/Results/`, `Tests/`, `tools/` klasörlerini içeren bir ilk commit oluştur.
3. **Summary** alanına örneğin şunu yaz:

   `Initial commit: EE3005 Assignment 2 image processing project`

4. **Commit to main** seç.

`.gitignore` çalışma zamanı klasörlerini, sanal Python ortamını ve geçici LaTeX dosyalarını dışlar. **Rapor PDF/DOCX ve `main.tex` kasıtlı olarak repository içindedir.**

## 4. GitHub'a publish / push

1. Üst bölümdeki **Publish repository** düğmesine bas.
2. Önerilen repository adı: `ee3005-image-processing-assignment-2`.
3. **Önemli:** Orijinal örnek görüntüler ve ödev PDF'inin kamuya açık dağıtım izni net değilse **Keep this code private** seçeneğini etkin bırak.
4. **Publish repository** ile yüklemeyi bitir.
5. GitHub üzerindeki README, `Report/` ve `MATLAB/` dosyalarını kontrol et.
6. Rapor içine eklenen bağlantının aynı hesaba ve repository adına karşılık geldiğini kontrol et: **https://github.com/burakcakirer/ee3005-image-processing-assignment-2**. Bu URL ancak repository yayınlandıktan sonra erişilebilir. Farklı bir repository adı veya kullanıcı adı seçersen rapordaki bağlantıyı da güncelle.

Sonraki güncellemelerde GitHub Desktop'ta **Changes → Commit to main → Push origin** adımlarını kullanabilirsin.

## 5. Teslim ve tutarlılık kontrolü

- Raporun Word sürümü: `Report/EE3005_Assignment2_Report.docx`
- Raporun PDF sürümü: `Report/EE3005_Assignment2_Report.pdf`
- Overleaf ana dosyası: `Report/main.tex` (yanında `Report/Figures` gerekli)
- MATLAB kaynak kodu: `MATLAB/run_assignment2.m`
- Python referans kodu: `Python_Reference/reproduce_results.py`

Raporda MATLAB/Python kaynak kodları **basılı halde yer almaz**. Kodlar dosya olarak ayrı durur; rapor metninde yalnızca ilgili dosyaların konumları, yöntemler ve analizler yer alır.

**Kontrol:** GitHub Desktop ile publish işlemi, MATLAB scriptini çalıştırmış veya raporu LMS'ye teslim etmiş olmak anlamına gelmez. MATLAB sonuçlarını yerel ortamında ayrıca üretmen ve dersin nihai teslim formatını kontrol etmen gerekir.
