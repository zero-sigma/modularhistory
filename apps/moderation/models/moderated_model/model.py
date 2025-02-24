import logging
from typing import TYPE_CHECKING, Optional

from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.moderation.constants import ModerationStatus
from apps.moderation.models.change.model import Change
from apps.moderation.models.contribution import ContentContribution
from apps.moderation.models.moderated_model.manager import ModeratedManager
from core.models.model import ExtendedModel
from core.models.soft_deletable import SoftDeletableModel

if TYPE_CHECKING:
    from django.db.models.fields import Field

    from apps.moderation.models.changeset import ChangeSet
    from apps.users.models import User


class ModeratedModel(SoftDeletableModel, ExtendedModel):
    """Base class for models of which instances must be moderated."""

    changes = GenericRelation(to='moderation.Change')

    # This field is used to determine whether model instances have been moderated and
    # should be visible to users.
    verified = models.BooleanField(
        verbose_name=_('verified'),
        default=False,
    )

    objects = ModeratedManager()

    class Meta:
        abstract = True

    class Moderation:
        excluded_fields = ['cache', 'date_string', 'changes', 'verified', 'deleted']

    def save_change(
        self,
        contributor: Optional['User'] = None,
        set: Optional['ChangeSet'] = None,
        parent_change: Optional['Change'] = None,
    ) -> Change:
        """Save changes to a `Change` instance."""
        object_is_new = self._state.adding
        self.clean()
        if object_is_new:
            self.verified = False
            self.save()
        change_in_progress = self.change_in_progress if not object_is_new else None
        if change_in_progress:
            # Save the changes to the existing in-progress `Change` instance.
            _change = change_in_progress
            ContentContribution.objects.create(
                contributor=contributor,
                change=_change,
                content_before=_change.changed_object,
                content_after=self,
            )
            _change.changed_object = self
            _change.set = set or _change.set  # TODO
            _change.parent = parent_change or _change.parent  # TODO
            _change.save()
        else:
            # Create a new `Change` instance.
            _change: Change = Change.objects.create(
                content_type=ContentType.objects.get_for_model(self.__class__),
                object_id=self.pk,
                moderation_status=ModerationStatus.PENDING,
                changed_object=self,
                set=set,
                parent=parent_change,
            )
            ContentContribution.objects.create(
                contributor=contributor,
                change=_change,
                content_before=_change.unchanged_object,
                content_after=self,
            )
        return _change

    @classmethod
    def get_moderated_fields(cls) -> list[dict]:
        """
        Return a serialized list of the model's moderated fields.

        This can be used to construct forms intelligently in front-end code.
        """
        fields = []
        field: 'Field'
        for field in cls._meta.get_fields():
            verbose_name = getattr(field, 'verbose_name', None)  # default to None
            editable = getattr(field, 'editable', True)  # default to True
            if any(
                [
                    field.name in cls.Moderation.excluded_fields,
                    not verbose_name or not editable,  # temporary heuristic -- TODO
                    field.name.endswith('_ptr'),  # OneToOneField
                ]
            ):
                continue
            fields.append(
                {
                    'name': field.name,
                    'verbose_name': verbose_name,
                    'editable': editable,
                    'choices': getattr(field, 'choices', None),
                    'help_text': getattr(field, 'help_text', None),
                    'type': field.__class__.__name__,
                }
            )
        return fields

    @property
    def change_in_progress(self) -> Optional['Change']:
        """Return the in-progress change for the moderated model instance."""
        return (
            self.changes.filter(moderation_status=ModerationStatus.PENDING).first()
            if self.has_change_in_progress
            else None
        )

    @property
    def has_change_in_progress(self) -> bool:
        """Return whether the moderated model instance has an in-progress change."""
        try:
            return self.changes.filter(moderation_status=ModerationStatus.PENDING).exists()
        except Exception as err:
            logging.error(err)
            return False
