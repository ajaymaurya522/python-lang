from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


class BaseEmailSponsorshipNotification:
    subject_template = None
    message_template = None
    email_context_keys = None

    def get_subject(self, context):
        return render_to_string(self.subject_template, context).strip()

    def get_message(self, context):
        return render_to_string(self.message_template, context).strip()

    def get_recipient_list(self, context):
        raise NotImplementedError

    def notify(self, **kwargs):
        context = {k: kwargs.get(k) for k in self.email_context_keys}

        email = EmailMessage(
            subject=self.get_subject(context),
            body=self.get_message(context),
            to=self.get_recipient_list(context),
            from_email=settings.SPONSORSHIP_NOTIFICATION_FROM_EMAIL,
        )
        email.send()


class AppliedSponsorshipNotificationToPSF(BaseEmailSponsorshipNotification):
    subject_template = "sponsors/email/psf_new_application_subject.txt"
    message_template = "sponsors/email/psf_new_application.txt"
    email_context_keys = ["request", "sponsorship"]

    def get_recipient_list(self, context):
        return [settings.SPONSORSHIP_NOTIFICATION_TO_EMAIL]


class AppliedSponsorshipNotificationToSponsors(BaseEmailSponsorshipNotification):
    subject_template = "sponsors/email/sponsor_new_application_subject.txt"
    message_template = "sponsors/email/sponsor_new_application.txt"
    email_context_keys = ["sponsorship"]

    def get_recipient_list(self, context):
        return context["sponsorship"].verified_emails


class RejectedSponsorshipNotificationToPSF(BaseEmailSponsorshipNotification):
    subject_template = "sponsors/email/psf_rejected_sponsorship_subject.txt"
    message_template = "sponsors/email/psf_rejected_sponsorship.txt"
    email_context_keys = ["sponsorship"]

    def get_recipient_list(self, context):
        return [settings.SPONSORSHIP_NOTIFICATION_TO_EMAIL]


class RejectedSponsorshipNotificationToSponsors(BaseEmailSponsorshipNotification):
    subject_template = "sponsors/email/sponsor_rejected_sponsorship_subject.txt"
    message_template = "sponsors/email/sponsor_rejected_sponsorship.txt"
    email_context_keys = ["sponsorship"]

    def get_recipient_list(self, context):
        return context["sponsorship"].verified_emails


# TODO add PDF attachment
class StatementOfWorkNotificationToPSF(BaseEmailSponsorshipNotification):
    subject_template = "sponsors/email/psf_statement_of_work_subject.txt"
    message_template = "sponsors/email/psf_statement_of_work.txt"
    email_context_keys = ["statement_of_work"]

    def get_recipient_list(self, context):
        return [settings.SPONSORSHIP_NOTIFICATION_TO_EMAIL]


# TODO add PDF attachment
class StatementOfWorkNotificationToSponsors(BaseEmailSponsorshipNotification):
    subject_template = "sponsors/email/sponsor_statement_of_work_subject.txt"
    message_template = "sponsors/email/sponsor_statement_of_work.txt"
    email_context_keys = ["statement_of_work"]

    def get_recipient_list(self, context):
        return context["statement_of_work"].sponsorship.verified_emails
