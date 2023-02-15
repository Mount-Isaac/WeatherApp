from django.shortcuts import render
from django.views import View
import json 
from urllib.request import urlopen

# Create your views here.
class homepage(View):
	template_name = "weatherdetector/index.html"
	
	def get(self, request, *args, **kwargs):
		return render(request, self.template_name, {})

	def post(self, request, *args, **kwargs):
		try:
			city = request.POST['city']
			if len(city) > 1:
				#rephrase city names with more than 1 word (New York -> New+York) to suit browser query format
				weather = urlopen(
					"http://api.openweathermap.org/data/2.5/weather?q="+city.replace(' ', '+')+"&appid=cb771e45ac79a4e8e2205c0ce66ff633"
					)
				json_data = json.loads(weather.read())
				# for keys, vals in json_data.items():
				# 		print(keys, vals)

				data = {
					"country_code": str(json_data['sys']['country']),
					"coordinate": str(json_data['coord']['lon']) + ' ' + str(json_data["coord"]["lat"]),
					"temp" : str(round(json_data["main"]["temp"]-273, 2)) + "°C",
					"pressure": str(json_data["main"]["pressure"]) + "Pa",
					"humidity": str(json_data["main"]["humidity"]) + "g.m-3"
				}
			else:
				#Null queries
				data = {}

			return render(request, self.template_name, data)

		# catch exception 
		except Exception as e:
			error = {
				"error_type": str(e).split(":")[1],
				"city": city
			}
			return render(request, self.template_name, error)

class error_404_view(View):
	template_name = 'weatherdetector/404.html'

	def get(self, request, exception):
		return render(request, self.template_name, {})
