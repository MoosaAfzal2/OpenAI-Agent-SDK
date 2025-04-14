import asyncio
import streamlit as st
from research_bot.manager import ResearchManager

async def fetch_research_result(query: str):
    result = await ResearchManager().run(query)
    return result


def main():
    st.title("Research Bot")
    st.write("Enter a topic you'd like to research, and get a detailed report!")

    query = st.text_input("Topic to research:")
    if st.button("Run Research"):
        if query.strip():
            with st.spinner("Researching..."):
                result = asyncio.run(fetch_research_result(query))
                st.subheader("Short Summary")
                st.write(result.short_summary)

                st.subheader("Markdown Report")
                st.markdown(result.markdown_report)

                st.subheader("Follow-Up Questions")
                st.write(result.follow_up_questions)
        else:
            st.error("Please enter a valid topic to research.")


if __name__ == "__main__":
    main()
