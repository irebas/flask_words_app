from models import *
from vars_libs import *
from functions_others import *


@app.route('/words/add_record_words.html', methods=['POST', 'GET'])
def add_record_words():
    """
    :return: adds record to Words database if record already doesn't exist
    """
    if request.method == 'POST':
        if request.form.get('save'):
            check_pl = Words.query.filter(Words.pl == request.form['pl']).first() is not None
            check_foreign = Words.query.filter(Words.foreign == request.form['foreign']).first() is not None
            if check_pl or check_foreign:
                flash('Such word already exists !')
                return redirect(url_for('add_record_words'))
            else:
                new_record = Words(request.form['words_group'], request.form['pl'].lower(),
                                   request.form['foreign'].lower(), request.form['label_1'].lower(),
                                   request.form['label_2'].lower(), date.today(), session['username'])
            db.session.add(new_record)
            db.session.commit()
            flash('Record added !')
            return redirect(url_for('add_record_words'))
    else:
        return render_template('/words/add_record_words.html')


@app.route('/words/manage_records_words.html', methods=['POST', 'GET'])
def manage_records_words():
    """
    :return: allows to modify or delete selected record
    """
    words_list = Words.query.order_by(Words.pl.asc()).all()
    if request.method == 'POST':
        if request.form.get('save'):
            selected_word = request.form['selected_word']
            record = Words.query.filter(Words.pl == selected_word).first()
            record.pl = request.form['pl']
            record.foreign = request.form['foreign']
            record.words_group = request.form['words_group']
            record.label_1 = request.form['label_1']
            record.label_2 = request.form['label_2']
            record.date = date.today()
            record.owner = session['username']
            db.session.commit()
            flash('Record modified!')
            return redirect(url_for('manage_records_words'))
        elif request.form.get('show'):
            selected_word = request.form['selected_word']
            words_group = Words.query.filter(Words.pl == selected_word).first().words_group
            pl = Words.query.filter(Words.pl == selected_word).first().pl
            foreign = Words.query.filter(Words.pl == selected_word).first().foreign
            label_1 = Words.query.filter(Words.pl == selected_word).first().label_1
            label_2 = Words.query.filter(Words.pl == selected_word).first().label_2
            return render_template('/words/manage_records_words.html', words_list=words_list,
                                   selected_word=selected_word, words_group=words_group,
                                   pl=pl, foreign=foreign, label_1=label_1, label_2=label_2)
        elif request.form.get('delete'):
            selected_word = request.form['selected_word']
            Words.query.filter(Words.pl == selected_word).delete()
            db.session.commit()
            return redirect(url_for('manage_records_words'))
    else:
        return render_template('/words/manage_records_words.html', words_list=words_list)


@app.route('/words/view_records_words.html', methods=['POST', 'GET'])
def view_records_words():
    """
    :return: table with words
    """
    if request.method == 'POST':
        if request.form.get('filter'):
            words_group = request.form['words_group']
            label_1 = request.form['label_1']
            label_2 = request.form['label_2']
            words_group = '%' + words_group + '%'
            label_1 = '%' + label_1 + '%'
            label_2 = '%' + label_2 + '%'
            words = Words.query.filter(Words.words_group.like(words_group), Words.label_2.like(label_2),
                                       Words.label_1.like(label_1)).all()
        else:
            words = Words.query.all()
    else:
        words = Words.query.all()

    label_1_list = [r.label_1 for r in db.session.query(Words.label_1).distinct()]
    label_2_list = [r.label_2 for r in db.session.query(Words.label_2).distinct()]
    label_1_list_new = create_unique_and_sorted_list(label_1_list)
    label_2_list_new = create_unique_and_sorted_list(label_2_list)

    return render_template('/words/view_records_words.html', label_1_list=label_1_list_new,
                           label_2_list=label_2_list_new, words=words)
