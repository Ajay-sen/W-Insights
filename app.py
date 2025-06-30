import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="W-Insights", layout="wide")
st.markdown("<h1 style='text-align: center; color: #915EFF;'>📊 W-Insights</h1>", unsafe_allow_html=True)

st.sidebar.title("Upload WhatsApp Chat File")
uploaded_file = st.sidebar.file_uploader("Choose a .txt file")

if uploaded_file is not None:
    st.sidebar.markdown(f"✅ **Uploaded File:** `{uploaded_file.name}`")
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show analysis for", user_list)

    if st.sidebar.button("Show Analysis"):
        st.markdown(f"### 👤 Analyzing chat for: **{selected_user}**")

        tab1, tab2, tab3, tab4 = st.tabs(["📈 Statistics", "📅 Timeline", "📊 Activity Map", "📦 Other Insights"])

        with tab1:
            num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
            st.subheader("Top Statistics")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Messages", num_messages)
            col2.metric("Total Words", words)
            col3.metric("Media Shared", num_media_messages)
            col4.metric("Links Shared", num_links)

        with tab2:
            st.subheader("Monthly Timeline")
            timeline = helper.monthly_timeline(selected_user, df)
            fig, ax = plt.subplots()
            fig.set_size_inches(5, 3)
            ax.plot(timeline['time'], timeline['message'], color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            st.subheader("Daily Timeline")
            daily_timeline = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots()
            fig.set_size_inches(5, 3)
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with tab3:
            st.subheader("Most Active Days and Months")
            col1, col2 = st.columns(2)

            with col1:
                busy_day = helper.week_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                fig.set_size_inches(5, 3)
                ax.bar(busy_day.index, busy_day.values, color='purple')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                busy_month = helper.month_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                fig.set_size_inches(5, 3)
                ax.bar(busy_month.index, busy_month.values, color='orange')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            st.subheader("Weekly Activity Heatmap")
            user_heatmap = helper.activity_heatmap(selected_user, df)
            fig, ax = plt.subplots()
            fig.set_size_inches(5, 3)
            ax = sns.heatmap(user_heatmap)
            st.pyplot(fig)

        with tab4:
            if selected_user == 'Overall':
                st.subheader('Most Busy Users')
                x, new_df = helper.most_busy_users(df)
                col1, col2 = st.columns(2)
                with col1:
                    fig, ax = plt.subplots()
                    fig.set_size_inches(5, 3)
                    ax.bar(x.index, x.values, color='red')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                with col2:
                    st.dataframe(new_df)

            st.subheader("Word Cloud")
            df_wc = helper.create_wordcloud(selected_user, df)
            st.image(df_wc.to_array(), use_column_width=True)

            st.subheader("Most Common Words")
            most_common_df = helper.most_common_words(selected_user, df)
            fig, ax = plt.subplots()
            fig.set_size_inches(5, 3)
            ax.barh(most_common_df[0], most_common_df[1])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            st.subheader("Emoji Analysis")
            emoji_df = helper.emoji_helper(selected_user, df)
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig, ax = plt.subplots()
                fig.set_size_inches(4, 4)
                ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
                st.pyplot(fig)
