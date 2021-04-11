import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as pxe
with st.echo(code_location='below'):
    st.set_option('deprecation.showPyplotGlobalUse', False)
    #визуал
    page = st.sidebar.selectbox("Выбери страницу", ["Различные графики", "Анимация по дням"])
    # данные
    df = pd.read_csv(r'/Users/nim/Documents/country_wise_latest.csv')
    df1=pd.read_csv(r'/Users/nim/Documents/full_grouped 2.csv')
    df1["Date"] = pd.to_datetime(df1["Date"],errors="coerce").dt.strftime("%Y-%m-%d")
    #новый датафрейм для одной страны, чтобы посмотроить потом график
    def get_new(df):
        nd = pd.DataFrame({
            'Status': ['Confirmed', 'Recovered', 'Deaths', 'Active'],
            'Number': (df.iloc[0]['Confirmed'],
                       df.iloc[0]['Recovered'],
                       df.iloc[0]['Deaths'],
                       df.iloc[0]['Active'])})
        return nd
    # создание табличек и графиков
    if page == 'Различные графики':
        st.title ("Различные данные по Covid-19")
        st.write('Здесь вы можете посмотреть различные графики по странам и случаям')
        visual=st.selectbox('Выберите график',('Гистограмма','Круговая диаграмма','Линейный график','Другое'))
        if visual=='Гистограмма':
            co_select = st.selectbox('Выберите страну', df['Country/Region'].unique())
            selected_c = df[df['Country/Region'] == co_select]
            country = get_new(selected_c)
            fig=pxe.bar(country,x='Status', y='Number', labels ={'Number':'Количество случаев в %s'%(co_select)}, color='Status')
            st.plotly_chart(fig)
        elif visual=='Круговая диаграмма':
            status = st.radio('Статус', ('Подтверждено', 'Сейчас', 'Выздоровели', 'Умерли'))
            countries = st.multiselect('Выберите страны',
                                       df['Country/Region'].unique())
            new_df=df[df['Country/Region'].isin(countries)]
            if status == 'Подтверждено':
                st.title("Все подтвержденные случаи")
                labels= new_df['Country/Region']
                values = new_df['Confirmed']
                fig, ax1 = plt.subplots()
                ax1.pie(values, autopct='%1.1f%%')
                ax1.axis('equal')
                ax1.legend(labels,
                      title="Страны",
                      loc="center left",
                      bbox_to_anchor=(1, 0, 0.5, 1))
                plt.tight_layout()
                st.pyplot(fig)
            elif status == 'Сейчас':
                st.title("Все текущие случаи")
                labels= new_df['Country/Region']
                values = new_df['Active']
                fig, ax1 = plt.subplots()
                ax1.pie(values, autopct='%1.1f%%')
                ax1.axis('equal')
                ax1.legend(labels,
                      title="Страны",
                      loc="center left",
                      bbox_to_anchor=(1, 0, 0.5, 1))
                plt.tight_layout()
                st.pyplot(fig)
            elif status == 'Выздоровели':
                st.title("Все случаи выздоровления")
                labels = new_df['Country/Region']
                values = new_df['Recovered']
                fig, ax1 = plt.subplots()
                ax1.pie(values, autopct='%1.1f%%')
                ax1.axis('equal')
                ax1.legend(labels,
                       title="Страны",
                       loc="center left",
                       bbox_to_anchor=(1, 0, 0.5, 1))
                plt.tight_layout()
                st.pyplot(fig)
            elif status == 'Умерли':
                st.title("Все случаи смерти")
                labels = new_df['Country/Region']
                values = new_df['Deaths']
                fig, ax1 = plt.subplots()
                ax1.pie(values, autopct='%1.1f%%')
                ax1.axis('equal')
                ax1.legend(labels,
                       title="Страны",
                       loc="center left",
                       bbox_to_anchor=(1, 0, 0.5, 1))
                plt.tight_layout()
                st.pyplot(fig)
        elif visual=='Линейный график':
            try:
                status = st.radio('Статус', ('Подтверждено', 'Сейчас', 'Выздоровели', 'Умерли'))
                countries = st.multiselect('Выберите страны',
                                  df1['Country/Region'].unique())
                new_df = df1[df1['Country/Region'].isin(countries)]
                if status == 'Подтверждено':
                    fig=pxe.line(new_df, x='Date', y='Confirmed', color='Country/Region')
                    st.plotly_chart(fig)
                elif status == 'Сейчас':
                    fig=pxe.line(new_df, x='Date', y='Active', color='Country/Region')
                    st.plotly_chart(fig)
                elif status == 'Выздоровели':
                    fig=pxe.line(new_df, x='Date', y='Recovered', color='Country/Region')
                    st.plotly_chart(fig)
                elif status == 'Умерли':
                    fig=pxe.line(new_df, x='Date', y='Deaths', color='Country/Region')
                    st.plotly_chart(fig)
            except KeyError:
                st.write('Выбери сначала страну :)')
        elif visual=='Другое':
            co_select = st.selectbox('Выберите страну', df1['Country/Region'].unique())
            st.write("Давайте посмотрим на гистограмму, которая показывает возможные состояния в данной стране")
            dff = df1[df1['Country/Region'] == co_select]
            fig, axs = plt.subplots(2, 2, figsize=(7, 7))
            sns.histplot(data=dff, x='Date', y="Confirmed", kde=True, ax=axs[0, 0])
            sns.histplot(data=dff,x='Date', y="Active", kde=True, ax=axs[0, 1])
            sns.histplot(data=dff,x='Date', y="Recovered", kde=True, ax=axs[1, 0])
            sns.histplot(data=dff,x='Date', y="Deaths", kde=True, ax=axs[1, 1])
            st.pyplot(fig)
    # создание анимации по смертям и выздоровевшим
    if page == 'Анимация по дням':
        st.title("Статистика по дням")
        st.write("Здесь вы можете выбрать дату и посмотреть как менялась статистика по выбранным аднным вплоть до этого месяца")
        visual=st.selectbox('Выберите сравнение',('По странам','Внутри одной страны'))
        if visual=='По странам':
            status = st.radio('Статус', ('Подтверждено', 'Сейчас', 'Выздоровели', 'Умерли'))
            countries = st.multiselect('Выберите страны',
                                       df['Country/Region'].unique())
            df2=df1[df1['Country/Region'].isin(countries)]
            try:
                if status == 'Подтверждено':
                    fig = pxe.bar(df2, x="Country/Region", y="Confirmed", color="Country/Region",
                        animation_frame="Date")
                    st.plotly_chart(fig)
                elif status == 'Сейчас':
                    fig = pxe.bar(df2, x="Country/Region", y="Active", color="Country/Region",
                        animation_frame="Date")
                    st.plotly_chart(fig)
                elif status == 'Умерли':
                    fig = pxe.bar(df2, x="Country/Region", y="Deaths", color="Country/Region",
                        animation_frame="Date")
                    st.plotly_chart(fig)
                elif status == 'Выздоровели':
                    fig = pxe.bar(df2, x="Country/Region", y="Recovered", color="Country/Region",
                        animation_frame="Date")
                    st.plotly_chart(fig)
            except KeyError:
                st.write('Выбери сначала страны, а потом двигайся по дням или смотри анимацию :)')
        elif visual == 'Внутри одной страны':
            co_select = st.selectbox('Выберите страну', df['Country/Region'].unique())
            st.write("Здесь должна была быть анимация для одной страны, но ее съели пингвины, поэтому посмотри и поиграйся с анимацией на предыдущей странице, там можно и только одну выбрать")
            hmm = st.selectbox('А что у нас тут?', ('?','Не понятно'))
            if hmm== 'Не понятно':
                st.write("Здесь нет анимации, но есть просто прикольные графики для выбранной страны")
                selected_c = df[df['Country/Region'] == co_select]
                d = get_new(selected_c)
                fig = pxe.bar(d, x='Status', y='Number', labels={'Number': 'Количество случаев в %s' % (co_select)},
                              color='Number')
                fig.update_layout(barmode='stack')
                st.plotly_chart(fig)
                st.write("Прирост новых случаев на каждый день")
                sel=df1[df1['Country/Region'] == co_select]
                sns.barplot(data=sel, x="Date", y="New cases")
                st.pyplot()
                st.write("А давайте посмотрим на взаимосвязи всего между всем. Интересно? А там и нет никакой взаимосвязи, но график забавный :)")
                sns.pairplot(selected_c)
                st.pyplot()