from flask_wtf import FlaskForm
from wtforms import SearchField, SelectMultipleField, StringField, SubmitField, widgets


class MultiCheckboxField(SelectMultipleField):

    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class QuickBookingForm(FlaskForm):

    bookingToMakeList = MultiCheckboxField('Reasons', coerce=int)
    submit = SubmitField()