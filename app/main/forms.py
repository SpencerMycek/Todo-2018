from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length
from datetime import datetime
from flask_babel import _, lazy_gettext as _l


class TodoForm(FlaskForm):
    todo = TextAreaField(_l('What needs to be done'), validators=[
        DataRequired(), Length(min=1, max=140)])
    month = SelectField(_l('Month'),
                        choices=[('Jan', _l('January')), ('Feb', _l('February')), ('Mar', _l('March')),
                                 ('Apr', _l('April')), ('May', _l('May')), ('Jun', _l('June')),
                                 ('Jul', _l('July')), ('Aug', _l('August')), ('Sep', _l('September')),
                                 ('Oct', _l('October')), ('Nov', _l('November')), ('Dec', _l('December'))],
                        validators=[DataRequired()])
    day_choice = [('1', _l('1')), ('2', _l('2')), ('3', _l('3')), ('4', _l('4')),
                  ('5', _l('5')), ('6', _l('6')), ('7', _l('7')),
                  ('8', _l('8')), ('9', _l('9')), ('10', _l('10')), ('11', _l('11')),
                  ('12', _l('12')), ('13', _l('13')), ('14', _l('14')),
                  ('15', _l('15')), ('16', _l('16')), ('17', _l('17')), ('18', _l('18')),
                  ('19', _l('19')), ('20', _l('20')), ('21', _l('21')),
                  ('22', _l('22')), ('23', _l('23')), ('24', _l('24')), ('25', _l('25')),
                  ('26', _l('26')), ('27', _l('27')), ('28', _l('28')),
                  ('29', _l('29')), ('30', _l('30')), ('31', _l('31'))]
    day = SelectField(_l("Day"), choices=day_choice, validators=[DataRequired()])
    year_num = datetime.utcnow().year
    year_choice = []
    for i in range(year_num, year_num + 5, 1):
        year_tuple = (str(i), str(i))
        year_choice.append(year_tuple)
    year = SelectField(_l("Year"), choices=year_choice, validators=[DataRequired()])
    hour = SelectField(_l("Time"), choices=day_choice[0:12:], validators=[DataRequired()])
    minute = SelectField(_l("Minute"), choices=[('0', '0'), ('15', '15'), ('30', '30'), ('45', '45')],
                         validators=[DataRequired()])
    a_p = SelectField(_l("AM or PM"), choices=[('AM', _l('AM')), ('PM', _l('PM'))], validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
