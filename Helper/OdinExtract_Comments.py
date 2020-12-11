# %% Admin
import pandas as pd

# %% Comment Extraction
def ExtractComments_viaSubmission(Conn_Object, SubmissionID_str):
    # Extraction- Submission Information
    # Conn_Object= Conn_Odin; SubmissionID_str= "k00ype"
    TempQuery_SubmissionInfo= "SELECT ID_Submission, CreatedDate, Title FROM Submission_Info " \
                               "WHERE ID_Submission='{}'".format(SubmissionID_str)
    SubmissionInfo = pd.read_sql_query(TempQuery_SubmissionInfo, Conn_Object)

    print("Extracting Comments from Submission {}: {}".format(SubmissionID_str,
                                                             SubmissionInfo.iloc[0]["Title"]))

    # Extraction- Comments
    TempQuery_Comments = "SELECT CI.ID_Comment, CI.ID_Submission, CI.created_utc, C.body " \
                          "FROM Comment_Information CI LEFT JOIN Comment C on CI.ID_Comment = C.ID_Comment " \
                          "WHERE ID_Submission='{}'".format(SubmissionID_str)
    Comments = pd.read_sql_query(TempQuery_Comments, Conn_Object)

    # Extraction- Submission Tracking
    TempQuery_IsClose= "SELECT ID_Submission, sum(IsClosed) as IsClosed FROM Submission_Tracking " \
                       "WHERE ID_Submission='{}' GROUP BY ID_Submission".format(SubmissionID_str)
    SubmissionTracking = pd.read_sql_query(TempQuery_IsClose, Conn_Object)
    Comments["IsClosed"]=0
    Comments.at[Comments.index[-1], "IsClosed"]= SubmissionTracking.iloc[0]["IsClosed"]

    # Merge and Processing
    Comments2=pd.merge(left=Comments, right=SubmissionInfo, on="ID_Submission", how="left")
    Comments2[['created_utc', 'CreatedDate']] = Comments2[['created_utc', 'CreatedDate']].apply(pd.to_datetime)
    Comments_Final=Comments2.reset_index(drop=True).copy()

    return Comments_Final
