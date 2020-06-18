from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import BaseBotForm, EditEconomyBotForm, ActionForm, ActionFormLoader
from app.utils import BotConfigBuilder, FormSelector, ConfigAlreadyExists


@app.route('/')
def index():
    if BotConfigBuilder.load_bot_config():
        display_delete_button = True
    else:
        display_delete_button = False

    return render_template('index.html', display_delete_button=display_delete_button)


@app.route('/new', methods=['GET', 'POST'])
def new():
    if BotConfigBuilder.config_already_exists():
        flash('Bot configuration already exists! Remove the old configuration before attempting to create a new one.', 'danger')
        return redirect(url_for('index'))

    form = BaseBotForm()

    if form.validate_on_submit():
        try:
            BotConfigBuilder.build_new(form)
            flash('Bot configuration created successfully!', 'success')

            return redirect(url_for('edit'))
        except ConfigAlreadyExists:
            flash(
                'Bot configuration was not created. Existing configuration could not be overwritten.', 'danger')
            flash(
                'If the problem persists, try deleting your existing configuration.', 'danger')

            return redirect(url_for('index'))

    return render_template('new.html', form=form)


@app.route('/delete', methods=['GET'])
def delete():
    BotConfigBuilder.delete_bot_config()

    if BotConfigBuilder.config_already_exists():
        flash('Bot configuration could not be deleted. Please try again.', 'danger')
    else:
        flash('Bot configuration was deleted successfully.', 'success')

    return redirect(url_for('index'))


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        form_data = request.form.to_dict()

        BotConfigBuilder.build_from_form(form_data)

        flash('Bot configuration was successfully updated.', 'success')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        if not BotConfigBuilder.config_already_exists():
            flash(
                'No existing configuration found! Please create a new configuration before modifying.', 'danger')

            return redirect(url_for('index'))

        bot_config = BotConfigBuilder.load_bot_config()
        form_class = FormSelector.select_form_for_bot_type(
            bot_config['handler'])
        ActionFormLoader(form_class).load_action_fields()
        form = form_class()
        subforms = [getattr(form, subform)
                    for subform in form.data if subform not in BotConfigBuilder.ignorable_view_fields()]

        return render_template('edit.html', name=bot_config['reddit']['username'], form=form, subforms=subforms)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500
