# %% Admin
import pandas as pd
from Helper.Source import connect_to_db


# %% Function Creations
def AllSubmissions_Table(conn_Object):
    # conn_Object= connect_to_db()

    # %% Submission Extraction
    # Submission Tracking Table
    TempQuery= "SELECT ID_Subreddit, ID_Submission, LastFetched, Numcomments, IsClosed FROM Submission_Tracking"
    SubmissionsTracking_Raw = pd.read_sql_query(TempQuery, conn_Object)
    SubmissionsTracking=SubmissionsTracking_Raw.copy()

    SubmissionsTracking["LastFetched"]= pd.to_datetime(SubmissionsTracking["LastFetched"])
    SubmissionsTracking2= SubmissionsTracking[["ID_Subreddit", "ID_Submission", "LastFetched","NumComments", "IsClosed"]].\
        sort_values('LastFetched').groupby(["ID_Subreddit","ID_Submission"]).\
        agg({"LastFetched":"last",
             "NumComments":"last",
             "IsClosed":"last"}).reset_index()

    # Additional Submission Information
    TempQuery_SubmissionInfo= "SELECT SI.ID_Submission, SI.CreatedDate, SI.Title, SI.URL FROM Submission_Info SI"
    SubmissionInfo_Raw = pd.read_sql_query(TempQuery_SubmissionInfo, conn_Object)
    SubmissionInfo_Raw["CreatedDate"]= pd.to_datetime(SubmissionInfo_Raw["CreatedDate"])

    TempQuery_SubredditInfo = "SELECT SI.ID_Subreddit, SI.Name as Subreddit FROM Subreddit_Info SI"
    Subreddit_Raw = pd.read_sql_query(TempQuery_SubredditInfo, conn_Object)

    # Consolidating Information
    Submissions_All = pd.merge(left=SubmissionsTracking2, right=SubmissionInfo_Raw, on="ID_Submission", how="outer")
    Submissions_All = pd.merge(left=Submissions_All, right=Subreddit_Raw,on="ID_Subreddit", how="outer")
    Submissions_All = Submissions_All.drop('ID_Subreddit', 1)

    # %% Returning
    Submissions_All_Final=Submissions_All[["Subreddit", "ID_Submission", "IsClosed",
                                           "CreatedDate","Title",
                                           "NumComments","URL"]]
    return(Submissions_All_Final)

