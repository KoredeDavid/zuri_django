from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.core.validators import MinLengthValidator
from ckeditor.fields import RichTextField


# This is to prevent unwanted characters so as not to disturb the web url
def clean_slug(value):
    clean_value = list(value)
    for i in clean_value:
        if not (i.isdigit() or i.isalpha() or i == ' '):
            clean_value.remove(i)
    return ''.join(clean_value)



username_validator = validators.RegexValidator( regex = r'^[\w]+\Z',
    message = _(
        'Enter a valid username. This value may contain only letters, '
        'numbers, and underscore.'
    ),
    flags = 0)


class CustomUser(AbstractUser):
    username = models.CharField(
        _('username'),
        max_length=30,
        help_text=_('Letters, digits and underscore only.'),
        unique=True,
        validators=[username_validator, MinLengthValidator(5)],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    is_author = models.BooleanField(default=False, )

    # This will be used for authors who are good enough not to need approval before their article gets published
    is_pro_author = models.BooleanField(default=False,)
    is_boss = models.BooleanField(default=False)
    email = models.EmailField(_('email address'), blank=False, null=True, unique=True)
    display_name = models.CharField(max_length=30, editable=False)

    def clean(self):
        # This raises a validation error because it makes no sense to make someone a pro_author if he/she aint an author
        if self.is_pro_author and not self.is_author:
            raise ValidationError('The user cannot be a professional author if he/she is not an author')

    def save(self, *args, **kwargs):
        self.clean()
        if self.email is not None:
            self.email = self.email.lower()
        if self.is_boss:
            print(True)
            self.is_author = True
            self.is_pro_author = True
        if self.username is not None:
            try:
                user = CustomUser.objects.get(id=self.id).username
            except CustomUser.DoesNotExist:
                user = None

            if self.username != user:
                self.display_name = self.username
                self.username = self.username.capitalize()

        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=50, editable=False)
    about = models.CharField(max_length=150)
    slug = models.SlugField(blank=True, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if self.name is not None:
            try:
                category = Category.objects.get(id=self.id).name
            except Category.DoesNotExist:
                category = None
            if self.name != category:
                self.display_name = self.name
                self.name = self.name.lower()
                self.slug = slugify(clean_slug(self.name))

        super().save(*args, **kwargs)

    def __str__(self):
        return self.display_name


def author_validation(value):
    user = CustomUser.objects.get(id=value)
    if not user.is_author:
        raise ValidationError('The user must be an author')


def approved_by_validation(value):
    user = CustomUser.objects.get(id=value)
    if not user.is_boss:
        raise ValidationError('Posts can only be approved by bosses')


class Post(models.Model):
    category = models.ForeignKey('Category', related_name='post', on_delete=models.CASCADE)
    title = models.CharField(max_length=50, unique=True)
    display_title = models.CharField(max_length=50, editable=False)
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE, validators=[author_validation, ],
                               related_name='post_author',  null=True)  #
    body = RichTextField()
    approved = models.BooleanField(default=False, )  #
    approved_by = models.ForeignKey('CustomUser', on_delete=models.CASCADE, validators=[approved_by_validation, ],
                                    related_name='post_approved_by', blank=True, null=True)  #
    published = models.BooleanField(default=False, )
    draft = models.BooleanField(default=False)  #
    liked_post = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, editable=False)

    def publish(self):
        self.draft = False
        self.published = True
        self.save()

    def save_as_draft(self):
        self.published = False
        self.draft = True
        self.save()

    def clean(self):
        print(self.author)
        if self.author:
            if self.author.is_pro_author:
                self.approved = True
        if not self.approved and self.approved_by is None and self.published:
            raise ValidationError("This post is yet to be approved by the boss, so it can't be published")

    def save(self, *args, **kwargs):
        self.clean()
        if self.title is not None:
            try:
                post = Post.objects.get(id=self.id).title
            except Post.DoesNotExist:
                post = None

            if self.title != post:
                self.display_title = self.title
                self.title = self.title.lower()
                self.slug = slugify(clean_slug(self.title))

        super().save(*args, **kwargs)

    def __str__(self):
        return self.display_title


class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = RichTextField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.author
