from flask import Flask, render_template, request, redirect, url_for
from api import SearcherConnection

import requests
import json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def show_signup_form():
	result = []
	searcher = SearcherConnection.getInstance()
	form = request.form
	total_result = 0
	rango = []
	if request.method == 'POST':
		if request.form['search'] == 'Buscar':
			name = request.form['name']
			content = request.form['content']
			efect_adv = request.form['efectos']
			envases = request.form['envases']
			alertas_comp = request.form.getlist("alertas_comp")
			result = searcher.search(name, content, envases, efect_adv, alertas_comp)

		elif request.form['search'] == 'Aplicar':			
			prin_act = request.form.getlist("prin_act")
			result = searcher.aplicate_princ_act(prin_act)

		elif request.form['search'] == 'Limpiar':
			searcher.clean()

		elif request.form['search'] == 'Siguiente':
			result = searcher.next_page()

		elif request.form['search'] == 'Anterior':
			result = searcher.previous_page()

		total_result = searcher.get_total_result()
		rango = searcher.get_actual_interval()
	
	inputs = checked_alertas(searcher.get_all_data())
	aggs = checked_prin_act(searcher.get_aggs(), inputs)
	return render_template("search.html", form=form, result=result, inputs=inputs, aggs=aggs, total_result=total_result, rango=rango)

@app.route("/detalles/<id>")
def detalles(id):
	result = SearcherConnection.getInstance().obtein(id)
	return render_template("detalles.html",result=result)

def checked_alertas(inputs):
	checks = ['', '', '', '']
	for alerta in inputs['alertas_comp']:
		if alerta == 'Lactancia':
			checks[0] = 'checked'
		elif alerta == 'Embarazo':
			checks[1] = 'checked'
		elif alerta == 'Fotosensibilidad':
			checks[2] = 'checked'
		elif alerta == 'Conducción de vehículos/maquinaria':
			checks[3] = 'checked'
	inputs['alertas_comp'] = checks
	return inputs

def checked_prin_act(aggs, inputs):
	for pa in inputs['prin_act']:
		for agg in aggs:
			if agg['key'] == pa:
				agg['check'] = 'checked'
	return aggs

if __name__ == '__main__':
    app.run(host="0.0.0.0")