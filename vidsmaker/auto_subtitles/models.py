from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        user = self.create_user(
            email,
            password=password,
            **extra_fields
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    def natural_key(self):
        return dict(email=self.email)
    
    def __str__(self):
        return self.email

User._meta.get_field('email')._unique = True
User._meta.get_field('email')._blank = False
User._meta.get_field('username')._unique = False
User._meta.get_field('username')._blank = True
User._meta.get_field('username')._null = True


class Transcript(models.Model):

    fonts = [('Arial', 'Arial'), ('AvantGarde-Book', 'AvantGarde-Book'), ('AvantGarde-BookOblique', 'AvantGarde-BookOblique'), ('AvantGarde-Demi', 'AvantGarde-Demi'), ('AvantGarde-DemiOblique', 'AvantGarde-DemiOblique'), ('Bookman-Demi', 'Bookman-Demi'), ('Bookman-DemiItalic', 'Bookman-DemiItalic'), ('Bookman-Light', 'Bookman-Light'), ('Bookman-LightItalic', 'Bookman-LightItalic'),( 'Courier',  'Courier'), ('Courier-Bold', 'Courier-Bold'), ('Courier-BoldOblique', 'Courier-BoldOblique'), ('Courier-Oblique', 'Courier-Oblique'), ('fixed', 'fixed'), ('Helvetica',  'Helvetica'), ('Helvetica-Bold', 'Helvetica-Bold'), ('Helvetica-BoldOblique', 'Helvetica-BoldOblique'), ('Helvetica-Narrow', 'Helvetica-Narrow'), ('Helvetica-Narrow-Bold', 'Helvetica-Narrow-Bold'), ('Helvetica-Narrow-BoldOblique', 'Helvetica-Narrow-BoldOblique'), ('Helvetica-Narrow-Oblique', 'Helvetica-Narrow-Oblique'), ('Helvetica-Oblique', 'Helvetica-Oblique'), ('NewCenturySchlbk-Bold', 'NewCenturySchlbk-Bold'), ('NewCenturySchlbk-BoldItalic', 'NewCenturySchlbk-BoldItalic'), ('NewCenturySchlbk-Italic', 'NewCenturySchlbk-Italic'), ('NewCenturySchlbk-Roman', 'NewCenturySchlbk-Roman'), ('Palatino-Bold', 'Palatino-Bold'), ('Palatino-BoldItalic', 'Palatino-BoldItalic'), ('Palatino-Italic', 'Palatino-Italic'), ('Palatino-Roman', 'Palatino-Roman'), ('Symbol', 'Symbol'), ('Times-Bold', 'Times-Bold'), ('Times-BoldItalic', 'Times-BoldItalic'), ('Times-Italic', 'Times-Italic'), ('Times-Roman', 'Times-Roman')]

    transcript = models.TextField()
    font = models.CharField(max_length=255, default="Arial", choices=fonts)
    text_color = models.CharField(max_length=7, default="#FFFFFF")
    background_color = models.CharField(max_length=7, default="#000000")
    background_opacity = models.FloatField(default=0.6, validators=[MinValueValidator(0),MaxValueValidator(1)])
    text_size = models.IntegerField(default=20, validators=[MinValueValidator(0),MaxValueValidator(200)])

    def __str__(self):
        return self.transcript

class Document(models.Model):
    langs = [('af-ZA', 'Afrikaans (South Africa)'), ('sq-AL', 'Albanian (Albania)'), ('am-ET', 'Amharic (Ethiopia)'), ('ar-DZ', 'Arabic (Algeria)'), ('ar-BH', 'Arabic (Bahrain)'), ('ar-EG', 'Arabic (Egypt)'), ('ar-IQ', 'Arabic (Iraq)'), ('ar-IL', 'Arabic (Israel)'), ('ar-JO', 'Arabic (Jordan)'), ('ar-KW', 'Arabic (Kuwait)'), ('ar-LB', 'Arabic (Lebanon)'), ('ar-MA', 'Arabic (Morocco)'), ('ar-OM', 'Arabic (Oman)'), ('ar-QA', 'Arabic (Qatar)'), ('ar-SA', 'Arabic (Saudi Arabia)'), ('ar-PS', 'Arabic (State of Palestine)'), ('ar-TN', 'Arabic (Tunisia)'), ('ar-AE', 'Arabic (United Arab Emirates)'), ('ar-YE', 'Arabic (Yemen)'), ('hy-AM', 'Armenian (Armenia)'), ('az-AZ', 'Azerbaijani (Azerbaijan)'), ('eu-ES', 'Basque (Spain)'), ('bn-BD', 'Bengali (Bangladesh)'), ('bn-IN', 'Bengali (India)'), ('bs-BA', 'Bosnian (Bosnia and Herzegovina)'), ('bg-BG', 'Bulgarian (Bulgaria)'), ('my-MM', 'Burmese (Myanmar)'), ('ca-ES', 'Catalan (Spain)'), ('zh-HK', 'Chinese, Cantonese (Traditional Hong Kong)'), ('zh-CN', 'Chinese, Mandarin (Simplified, China)'), ('zh-TW', 'Chinese, Mandarin (Traditional, Taiwan)'), ('hr-HR', 'Croatian (Croatia)'), ('cs-CZ', 'Czech (Czech Republic)'), ('da-DK', 'Danish (Denmark)'), ('nl-BE', 'Dutch (Belgium)'), ('nl-NL', 'Dutch (Netherlands)'), ('en-AU', 'English (Australia)'), ('en-CA', 'English (Canada)'), ('en-GH', 'English (Ghana)'), ('en-HK', 'English (Hong Kong)'), ('en-IN', 'English (India)'), ('en-IE', 'English (Ireland)'), ('en-KE', 'English (Kenya)'), ('en-NZ', 'English (New Zealand)'), ('en-NG', 'English (Nigeria)'), ('en-PK', 'English (Pakistan)'), ('en-PH', 'English (Philippines)'), ('en-SG', 'English (Singapore)'), ('en-ZA', 'English (South Africa)'), ('en-TZ', 'English (Tanzania)'), ('en-GB', 'English (United Kingdom)'), ('en-US', 'English (United States)'), ('et-EE', 'Estonian (Estonia)'), ('il-PH', 'Filipino (Philippines)'), ('fi-FI', 'Finnish (Finland)'), ('fr-BE', 'French (Belgium)'), ('fr-CA', 'French (Canada)'), ('fr-FR', 'French (France)'), ('fr-CH', 'French (Switzerland)'), ('gl-ES', 'Galician (Spain)'), ('ka-GE', 'Georgian (Georgia)'), ('de-AT', 'German (Austria)'), ('de-DE', 'German (Germany)'), ('de-CH', 'German (Switzerland)'), ('el-GR', 'Greek (Greece)'), ('gu-IN', 'Gujarati (India)'), ('iw-IL', 'Hebrew (Israel)'), ('hi-IN', 'Hindi (India)'), ('hu-HU', 'Hungarian (Hungary)'), ('is-IS', 'Icelandic (Iceland)'), ('id-ID', 'Indonesian (Indonesia)'), ('it-IT', 'Italian (Italy)'), ('it-CH', 'Italian (Switzerland)'), ('ja-JP', 'Japanese (Japan)'), ('jv-ID', 'Javanese (Indonesia)'), ('kn-IN', 'Kannada (India)'), ('kk-KZ', 'Kazakh (Kazakhstan)'), ('km-KH', 'Khmer (Cambodia)'), ('ko-KR', 'Korean (South Korea)'), ('lo-LA', 'Lao (Laos)'), ('lv-LV', 'Latvian (Latvia)'), ('lt-LT', 'Lithuanian (Lithuania)'), ('mk-MK', 'Macedonian (North Macedonia)'), ('ms-MY', 'Malay (Malaysia)'), ('ml-IN', 'Malayalam (India)'), ('mr-IN', 'Marathi (India)'), ('mn-MN', 'Mongolian (Mongolia)'), ('ne-NP', 'Nepali (Nepal)'), ('no-NO', 'Norwegian Bokmål (Norway)'), ('fa-IR', 'Persian (Iran)'), ('pl-PL', 'Polish (Poland)'), ('pt-BR', 'Portuguese (Brazil)'), ('pt-PT', 'Portuguese (Portugal)'), ('pa-Gu', 'Punjabi (Gurmukhi India)'), ('ro-RO', 'Romanian (Romania)'), ('ru-RU', 'Russian (Russia)'), ('sr-RS', 'Serbian (Serbia)'), ('si-LK', 'Sinhala (Sri Lanka)'), ('sk-SK', 'Slovak (Slovakia)'), ('sl-SI', 'Slovenian (Slovenia)'), ('es-AR', 'Spanish (Argentina)'), ('es-BO', 'Spanish (Bolivia)'), ('es-CL', 'Spanish (Chile)'), ('es-CO', 'Spanish (Colombia)'), ('es-CR', 'Spanish (Costa Rica)'), ('es-DO', 'Spanish (Dominican Republic)'), ('es-EC', 'Spanish (Ecuador)'), ('es-SV', 'Spanish (El Salvador)'), ('es-GT', 'Spanish (Guatemala)'), ('es-HN', 'Spanish (Honduras)'), ('es-MX', 'Spanish (Mexico)'), ('es-NI', 'Spanish (Nicaragua)'), ('es-PA', 'Spanish (Panama)'), ('es-PY', 'Spanish (Paraguay)'), ('es-PE', 'Spanish (Peru)'), ('es-PR', 'Spanish (Puerto Rico)'), ('es-ES', 'Spanish (Spain)'), ('es-US', 'Spanish (United States)'), ('es-UY', 'Spanish (Uruguay)'), ('es-VE', 'Spanish (Venezuela)'), ('su-ID', 'Sundanese (Indonesia)'), ('sw-KE', 'Swahili (Kenya)'), ('sw-TZ', 'Swahili (Tanzania)'), ('sv-SE', 'Swedish (Sweden)'), ('ta-IN', 'Tamil (India)'), ('ta-MY', 'Tamil (Malaysia)'), ('ta-SG', 'Tamil (Singapore)'), ('ta-LK', 'Tamil (Sri Lanka)'), ('te-IN', 'Telugu (India)'), ('th-TH', 'Thai (Thailand)'), ('tr-TR', 'Turkish (Turkey)'), ('uk-UA', 'Ukrainian (Ukraine)'), ('ur-IN', 'Urdu (India)'), ('ur-PK', 'Urdu (Pakistan)'), ('uz-UZ', 'Uzbek (Uzbekistan)'), ('vi-VN', 'Vietnamese (Vietnam)'), ('zu-ZA', 'Zulu (South Africa)')]
    document = models.FileField(upload_to='documents/')
    name = models.CharField(null=True, blank=True, max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    size = models.FloatField(default=0.0)
    language = models.TextField(default="en-US", choices=langs)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transcript = models.ForeignKey(Transcript, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.document.path


# FREE = 1Gb - 60min video max
# 9;99 = 20Gb - 60min video max
# 29;99 = 100Gb - no limit + translation