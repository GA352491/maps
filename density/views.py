from django.shortcuts import render
import plotly.express as px
import json
import numpy as np
import pandas as pd


# Create your views here.
def home(request):
    india_states = json.load(open(r'density/static/states_india.geojson', 'r'))

    state_id_map = {}
    for feature in india_states["features"]:
        feature["id"] = feature["properties"]["state_code"]
        state_id_map[feature["properties"]["st_nm"]] = feature["id"]

    df = pd.read_excel(r'density/static/map.xlsx')

    df['Density'] = df['Density[a]'].apply(lambda x: int(x.split("/")[0].replace(",", "")))
    df["id"] = df["State or union territory"].apply(lambda x: state_id_map[x])

    # print(df.head())

    df["DensityScale"] = np.log10(df["Density"])

    df2 = df.where(df['Density'] > 500).dropna(how='all')
    # print(df2)

    fig = px.choropleth_mapbox(
        df,
        locations="id",
        geojson=india_states,
        color="DensityScale",
        hover_name="State or union territory",
        hover_data=["Density", "Population"],
        title="India Population Density",
        mapbox_style="carto-positron",
        center={"lat": 24, "lon": 78},
        zoom=3,
        opacity=0.5,
    )
    config = {'displaylogo': False}

    fig2 = fig.to_html(full_html=False, default_height=700, default_width=900, config=config)

    lis = df.keys()
    # print(lis)

    if request.method == 'POST':

        answer = request.POST.getlist('checks[]')
        answer2 = request.POST.getlist('text')
        answer3 = request.POST.getlist('checks2[]')

        # print(answer[0])
        # print(answer2[0])
        # print(answer3[0])
        # print(type(answer2[0]))

        if answer3[0] == '>':
            df2 = df.where(df[answer[0]] > int(answer2[0])).dropna(how='all')
        elif answer3[0] == '<':
            df2 = df.where(df[answer[0]] < int(answer2[0])).dropna(how='all')
        elif answer3[0] == '<=':
            df2 = df.where(df[answer[0]] <= int(answer2[0])).dropna(how='all')
        elif answer3[0] == '>=':
            df2 = df.where(df[answer[0]] >= int(answer2[0])).dropna(how='all')
        elif answer3[0] == '=':
            df2 = df.where(df[answer[0]] == int(answer2[0])).dropna(how='all')

            # if type(answer2[0]) == int:
            #     df2 = df.where(df[answer[0]] == int(answer2[0])).dropna(how='all')
            # else:
            #     df2 = df.where(df[answer[0]] == str(answer2[0])).dropna(how='all')

        # print(df2)
        fig = px.choropleth_mapbox(
            df2,
            locations='id',
            geojson=india_states,
            color="DensityScale",
            hover_name="State or union territory",
            hover_data=["Density", "Population", answer[0]],
            title="India Population Density",
            mapbox_style="carto-positron",
            center={"lat": 24, "lon": 78},
            zoom=3,
            opacity=0.5,
        )
        config = {'displaylogo': False}

        fig2 = fig.to_html(full_html=False, default_height=700, default_width=900, config=config)

        context = {'fig2': fig2, 'lis': lis}
        return render(request, 'home.html', context)

    context = {'fig2': fig2, 'lis': lis}

    return render(request, 'home.html', context)
