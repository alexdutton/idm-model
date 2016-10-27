from django.db import models

SEX_CHOICES = (
    ('0', 'not known'),
    ('1', 'male'),
    ('2', 'female'),
    ('9', 'not applicable'),
)

AFFILIATION_STATE_CHOICES = (
    ('offered', 'offered'),
    ('declined', 'declined'),
    ('forthcoming', 'forthcoming'),
    ('active', 'active'),
    ('historic', 'historic'),
    ('suspended', 'suspended'),
)

# Reference data

class OrganizationRelationshipType(models.Model):
    id = models.CharField(max_length=256, primary_key=True)
    label = models.CharField(max_length=256)


class NameContext(models.Model):
    id = models.CharField(max_length=256, primary_key=True)
    label = models.CharField(max_length=256)


class ImageContext(models.Model):
    id = models.CharField(max_length=256, primary_key=True)
    label = models.CharField(max_length=256)


class IdentifierType(models.Model):
    id = models.CharField(max_length=256, primary_key=True)
    label = models.CharField(max_length=256)


class NameComponentType(models.Model):
    id = models.CharField(max_length=256, primary_key=True)
    label = models.CharField(max_length=256)


class AffiliationType(models.Model):
    id = models.CharField(max_length=256, primary_key=True)
    label = models.CharField(max_length=256)


class RoleType(models.Model):
    id = models.CharField(max_length=256, primary_key=True)
    label = models.CharField(max_length=256)


class Country(models.Model):
    id = models.CharField(max_length=256, primary_key=True)
    label = models.CharField(max_length=256)


class ContactContext(models.Model):
    id = models.CharField(max_length=256, primary_key=True)
    label = models.CharField(max_length=256)


class SocialAccountProvider(models.Model):
    id = models.CharField(max_length=256, primary_key=True)
    label = models.CharField(max_length=256)


# Non-reference data


class Person(models.Model):
    id = models.UUIDField(primary_key=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='0')
    nationalities = models.ManyToManyField(Country)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)
    deceased = models.BooleanField(default=False)


class Image(models.Model):
    person = models.ForeignKey(Person)
    image = models.ImageField()
    contexts = models.ManyToManyField(ImageContext)


class Identifier(models.Model):
    person = models.ForeignKey(Person)
    type = models.ForeignKey(IdentifierType)
    value = models.CharField(max_length=255)
    

class Name(models.Model):
    person = models.ForeignKey(Person)
    contexts = models.ManyToManyField(NameContext)


class NameComponent(models.Model):
    name = models.ForeignKey(Name)
    type = models.ForeignKey(NameComponentType)
    value = models.CharField(max_length=255)


class Organization(models.Model):
    label = models.CharField(max_length=255)
    related_to = models.ManyToManyField('self', symmetrical=False, related_name='related_from', through='OrganizationRelationship')


class Account(models.Model):
    person = models.ForeignKey(Person, null=True, blank=True)
    organization = models.ForeignKey(Organization, null=True, blank=True)
    role_at_organization = models.ForeignKey('RoleAtOrganization', null=True, blank=True)
    primary = models.BooleanField()
    principal_name = models.CharField(max_length=255)


class OrganizationRelationship(models.Model):
    from_organization = models.ForeignKey(Organization, related_name='relationship_to')
    to_organization = models.ForeignKey(Organization, related_name='relationship_from')
    type = models.ForeignKey(OrganizationRelationshipType)


class Affiliation(models.Model):
    person = models.ForeignKey(Person)
    organization = models.ForeignKey(Organization)
    type = models.ForeignKey(AffiliationType)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    effective_start = models.DateTimeField(null=True, blank=True)
    effective_end = models.DateTimeField(null=True, blank=True)
    suspended = models.BooleanField(default=False)
    suspended_until = models.DateTimeField(null=True, blank=True)
    state = models.CharField(max_length=32, choices=AFFILIATION_STATE_CHOICES)


class Role(models.Model):
    person = models.ForeignKey(Person)
    organization = models.ForeignKey(Organization)
    type = models.ForeignKey(RoleType)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    effective_start = models.DateTimeField(null=True, blank=True)
    effective_end = models.DateTimeField(null=True, blank=True)
    suspended = models.BooleanField(default=False)
    suspended_until = models.DateTimeField(null=True, blank=True)
    state = models.CharField(max_length=32, choices=AFFILIATION_STATE_CHOICES)


class RoleAtOrganization(models.Model):
    organization = models.ForeignKey(Organization)
    type = models.ForeignKey(AffiliationType)
    label = models.CharField(max_length=255)


class Contact(models.Model):
    person = models.ForeignKey(Person, null=True, blank=True)
    organization = models.ForeignKey(Organization, null=True, blank=True)
    role_at_organization = models.ForeignKey(RoleAtOrganization, null=True, blank=True)
    context = models.ForeignKey(ContactContext)
    priority = models.PositiveSmallIntegerField()

    class Meta:
        abstract = True


class Email(Contact):
    address = models.EmailField()


class Telephone(Contact):
    number = models.CharField(max_length=32)


class Address(Contact):
    extended_address = models.CharField(max_length=32)
    street_address = models.CharField(max_length=32)
    locality = models.CharField(max_length=32)
    postal_code = models.CharField(max_length=32)
    country = models.ForeignKey(Country)


class SocialAccount(Contact):
    provider = models.ForeignKey(SocialAccountProvider)
    username = models.CharField(max_length=255)
    profile_url = models.URLField()

