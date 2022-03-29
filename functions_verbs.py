from models import *
from vars_libs import *
from functions_others import *


@app.route('/verbs/add_record_verbs.html', methods=['POST', 'GET'])
def add_record_verbs():
    """
    :return: adds record to Verbs database if record already doesn't exist
    """
    if request.method == 'POST':
        if request.form.get('save'):
            check_pl = Verbs.query.filter(Verbs.pl == request.form['pl']).first() is not None
            check_form1 = Verbs.query.filter(Verbs.form1 == request.form['form1']).first() is not None
            if check_pl or check_form1:
                flash('Such word already exists !')
                return redirect(url_for('add_record_verbs'))
            else:
                new_record = Verbs(request.form['verbs_group'], request.form['pl'].lower(),
                                   request.form['form1'].lower(), request.form['form2'].lower(),
                                   request.form['form3'].lower())
            db.session.add(new_record)
            db.session.commit()
            flash('Record added !')
            return redirect(url_for('add_record_verbs'))
        elif request.form.get('import'):
            file = request.files['file']
            directory = os.path.dirname(os.path.abspath(__file__))
            uploaded_file_path = os.path.join(directory, 'uploads', file.filename)
            file.save(uploaded_file_path)
            add_verbs_from_xlsx(uploaded_file_path)
            flash('File imported successfully!')
            return redirect(url_for('add_record_verbs'))
    else:
        return render_template('/verbs/add_record_verbs.html')


@app.route('/verbs/manage_records_verbs.html', methods=['POST', 'GET'])
def manage_records_verbs():
    """
    :return: allows to modify or delete selected record
    """
    verbs_list = Verbs.query.order_by(Verbs.form1.asc()).all()
    if request.method == 'POST':
        if request.form.get('save'):
            selected_verb = request.form['selected_verb']
            record = Verbs.query.filter(Verbs.pl == selected_verb).first()
            record.verbs_group = request.form['verbs_group']
            record.pl = request.form['pl'].lower()
            record.form1 = request.form['form1'].lower()
            record.form2 = request.form['form2'].lower()
            record.form3 = request.form['form3'].lower()
            db.session.commit()
            flash('Record modified!')
            return redirect(url_for('manage_records_verbs'))
        elif request.form.get('show'):
            selected_verb = request.form['selected_verb']
            verbs_group = Verbs.query.filter(Verbs.pl == selected_verb).first().verbs_group
            pl = Verbs.query.filter(Verbs.pl == selected_verb).first().pl
            form1 = Verbs.query.filter(Verbs.pl == selected_verb).first().form1
            form2 = Verbs.query.filter(Verbs.pl == selected_verb).first().form2
            form3 = Verbs.query.filter(Verbs.pl == selected_verb).first().form3
            return render_template('/verbs/manage_records_verbs.html', selected_verb=selected_verb,
                                   verbs_list=verbs_list, pl=pl, verbs_group=verbs_group, form1=form1,
                                   form2=form2, form3=form3)
        elif request.form.get('delete'):
            selected_verb = request.form['selected_verb']
            Verbs.query.filter(Verbs.pl == selected_verb).delete()
            db.session.commit()
            flash('Record deleted!')
            return redirect(url_for('manage_records_verbs'))
    else:
        return render_template('/verbs/manage_records_verbs.html', verbs_list=verbs_list)


@app.route('/verbs/view_records_verbs.html', methods=['POST', 'GET'])
def view_records_verbs():
    """
    :return: table with verbs. Allows to filter verbs by verbs_group.
    """
    if request.method == 'POST':
        if request.form.get('filter'):
            verbs_group = request.form['verbs_group']
            print(verbs_group)
            verbs_group = '%' + verbs_group + '%'
            verbs = Verbs.query.filter(Verbs.verbs_group.like(verbs_group)).order_by(Verbs.form1.asc()).all()
        else:
            verbs = Verbs.query.order_by(Verbs.form1.asc()).all()
    else:
        verbs = Verbs.query.order_by(Verbs.form1.asc()).all()
    return render_template('/verbs/view_records_verbs.html', verbs=verbs)


@app.route('/verbs/practice_verbs.html', methods=['POST', 'GET'])
def practice_verbs():
    """
    :return: allows to select number and group of verbs. Verbs are drawn in the separate function
    and there is created 3D array with following dimensions: verb_drawn / verb_provided_by_user / font_color.
    Results are compared and saved to VerbsResults DB.
    """
    if request.method == 'POST':
        if request.form.get('draw_verbs'):
            verbs_group = request.form['verbs_group']
            verbs_nb = int(request.form['verbs_nb'])
            verbs_array = get_verbs_to_play(verbs_group, verbs_nb)
            session['verbs_array'] = verbs_array
            session['verbs_nb'] = verbs_nb
            session['verbs_group'] = verbs_group
            flash('Verbs drawn!')
        elif request.form.get('check'):
            points = 0
            verbs_array = session['verbs_array']
            verbs_nb = session['verbs_nb']
            verbs_group = session['verbs_group']
            for i in range(verbs_nb):
                form1 = verbs_array[i][1][0].upper()
                form2 = verbs_array[i][2][0].upper()
                form3 = verbs_array[i][3][0].upper()
                user_form1 = request.form[form1].upper()
                user_form2 = request.form[form2].upper()
                user_form3 = request.form[form3].upper()
                if user_form1 == form1:
                    verbs_array[i][1][2] = 'green'
                    points = points + 1
                else:
                    verbs_array[i][1][2] = 'red'
                if user_form2 == form2:
                    verbs_array[i][2][2] = 'green'
                    points = points + 1
                else:
                    verbs_array[i][2][2] = 'red'
                if user_form3 == form3:
                    verbs_array[i][3][2] = 'green'
                    points = points + 1
                else:
                    verbs_array[i][3][2] = 'red'
                verbs_array[i][1][1] = user_form1
                verbs_array[i][2][1] = user_form2
                verbs_array[i][3][1] = user_form3
            result = str(points) + '/' + str(verbs_nb * 3)
            new_record = ResultsVerbs(session['username'], verbs_group,
                                      result, str(date.today()))
            db.session.add(new_record)
            db.session.commit()
            flash('You obtained: ' + result)
        return render_template('/verbs/practice_verbs.html', verbs_array=verbs_array, verbs_nb=verbs_nb,
                               verbs_group=verbs_group)
    else:
        return render_template('/verbs/practice_verbs.html')


def get_verbs_to_play(verbs_group, verbs_nb):
    """
    :param verbs_group: group of verbs (easy/medium/hard/mix etc)
    :type verbs_group: string
    :param verbs_nb: number of verbs
    :type verbs_nb: integer
    :return: 3D array of randomly drawn verbs
    :rtype: array
    """
    verbs_filtered = []
    verbs_all = Verbs.query.all()
    print(verbs_all)
    # verb_all_forms = [['' for k in range(4)] for j in range(verbs_nb)]
    if verbs_group == 'Mix':
        for verb in verbs_all:
            print(verb.pl + verb.form1 + verb.form2 + verb.form3)
            verb_all_forms = [[verb.pl, '', 'black'], [verb.form1, '', 'black'],
                              [verb.form2, '', 'black'], [verb.form3, '', 'black']]
            verbs_filtered.append(verb_all_forms)
    elif verbs_group == 'Easy_Medium':
        for verb in verbs_all:
            if verb.verbs_group == 'Easy' or verb.verbs_group == 'Medium':
                verb_all_forms = [[verb.pl, '', 'black'], [verb.form1, '', 'black'],
                                  [verb.form2, '', 'black'], [verb.form3, '', 'black']]
                verbs_filtered.append(verb_all_forms)
    elif verbs_group == 'Medium_Hard':
        for verb in verbs_all:
            if verb.verbs_group == 'Medium' or verb.verbs_group == 'Hard':
                verb_all_forms = [[verb.pl, '', 'black'], [verb.form1, '', 'black'],
                                  [verb.form2, '', 'black'], [verb.form3, '', 'black']]
                verbs_filtered.append(verb_all_forms)
    else:
        for verb in verbs_all:
            if verb.verbs_group == verbs_group:
                verb_all_forms = [[verb.pl, '', 'black'], [verb.form1, '', 'black'],
                                  [verb.form2, '', 'black'], [verb.form3, '', 'black']]
                verbs_filtered.append(verb_all_forms)

    verbs_to_play = random.sample(verbs_filtered, verbs_nb)
    return verbs_to_play


@app.route('/verbs/view_results_verbs.html', methods=['POST', 'GET'])
def view_results_verbs():
    """
    :return: table with results. Allows to filter on username
    """
    users_list = [r.username for r in db.session.query(ResultsVerbs.username).distinct()]
    users_list_new = create_unique_and_sorted_list(users_list)
    if request.method == 'POST':
        if request.form.get('filter'):
            username = request.form['username']
            username = '%' + username + '%'
            results = ResultsVerbs.query.filter(ResultsVerbs.username.like(username)).order_by(ResultsVerbs.date.asc()).all()
        else:
            results = ResultsVerbs.query.order_by(ResultsVerbs.date.asc()).all()
    else:
        results = ResultsVerbs.query.order_by(ResultsVerbs.date.asc()).all()

    return render_template('/verbs/view_results_verbs.html', results=results, users_list=users_list_new)


def add_verbs_from_xlsx(file_path):
    """
    :param file_path: file path
    :type file_path: Creates list of tuples. Each tuple stands for one verb. Omits first row with headers.
    """
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    verbs_list = []
    k = 0
    for row in sheet.iter_rows():
        k = k + 1
        if k > 1:
            verbs_list.append((row[0].value, row[1].value, row[2].value, row[3].value, row[4].value))

    for verb in verbs_list:
        new_verb = Verbs(verb[0], verb[1], verb[2], verb[3], verb[4])
        db.session.add(new_verb)
        db.session.commit()
