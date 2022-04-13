

from email import message
from turtle import color


def html_isbot(id_bot, type_bot, datetime, Label_API, status):

    date_time = datetime

    id = ""
    id = str(id_bot)
    type_ = str(type_bot)
    if status == "stop":
        ids = "pause_bot_"+id
        color = "alert-dark"
        message_ = " data-bs-mess_title='Bot Start' data-bs-mess_body='Are you sure Start ?' "
    else:
        ids = "running_bot_"+id
        color = "alert-success"
        message_ = " data-bs-mess_title='Bot Pause' data-bs-mess_body='Are you sure Pause ?' "
    if str(status) == "stop":
        icon = "bell-off"
    else:
        icon = "bell"
    if type_ == "Future":
        future_option = """  <div class="mb-0">
                                                <div class="text-success">

                                                    Long alert: 59
                                                    Close Long : 59 
                                                </div>

                                                <div class="text-danger">

                                                    Short alert: 58 
                                                    Close Short : 58 
                                                </div>

                                                <div><span class="text-muted">Start date: """+str(date_time) + """</span></div>
                                            </div>"""
    else:
        future_option = """  <div class="mb-0">
                                                <div class="text-success">

                                                    Buy alert: 59
                                                </div>

                                                <div class="text-danger">

                                                    Sell alert: 58
                                                </div>

                                                <div><span class="text-muted">Start date: """+str(date_time) + """</span></div>
                                            </div>"""
    html2 = """ <div class="row ">
                                    <div class="card">
                                        <div class="card-body">
                                            <div class="row">
                                                <nav class="navbar navbar-light """+color+""" m-0 p-0">
                                                    <div class="container-fluid m-0 p-0">
                                                        <a class="navbar-brand">"""+str(Label_API) + """</a>
                                                        <form class="d-flex" method="POST">

                                                            <a class="nav-icon dropdown-toggle" id="detail_Bot_"""+id+"""" onClick="reply_click(this.id)" data-bs-toggle="modal" data-bs-target="#detail_Bot_"""+id+"""modal">
                                                                <div class="position-relative justify-content-md-end">
                                                                    <i class="align-middle mx-0" data-feather="help-circle"></i>

                                                                </div>
                                                            </a>

                                                            <a class="nav-icon dropdown-toggle" id="""+ids+""" onClick="reply_click(this.id)" data-bs-toggle="modal" data-bs-target="#pause_bot_Modal" """+message_+""">
                                                                <div class="position-relative justify-content-md-end">
                                                                    <i class="align-middle mx-0" data-feather="""+icon+""" ></i>

                                                                </div>
                                                            </a>



                                                            <a class="nav-icon dropdown-toggle" id="delete_bot_"""+id+"""" onClick="reply_click(this.id)" data-bs-toggle="modal" data-bs-target="#delete_bot_Modal">
                                                                <div class="position-relative justify-content-md-end">
                                                                    <i class="align-middle mx-0" data-feather="trash-2"></i>

                                                                </div>
                                                            </a>
                                                        </form>

                                                    </div>
                                                </nav>
                                            </div>

                                            <div class="row">

                                                <h3 class="mt-1 mb-3">"""+str(type_) + """</h3>

                                            </div>

                                           """+future_option+"""
                                        </div>
                                    </div>
                                </div>"""

    return html2


def html_modal(id_bot, type_bot, MarginType, ReOpenOrder, Label_API, API_Key, API_SECRET, LineNotify, PassPhrase):

    id = ""
    id = str(id_bot)
    idx = id+"_"
    type_ = str(type_bot)

    if MarginType == "ISOLATED":
        MarginType_ = """<ul onChange="add_text(this.id)" id="""+idx+"""MarginType><li><input id="MarginType-0" name="""+idx+"""MarginType type="radio" value="ISOLATED" checked> <label for="MarginType-0">ISOLATED</label></li><li><input id="MarginType-1" name=""" + \
            idx+"""MarginType type="radio" value="CROSSED"> <label for="MarginType-1">CROSSED</label></li></ul>"""
    elif MarginType == "CROSSED":
        MarginType_ = """<ul onChange="add_text(this.id)" id="""+idx+"""MarginType><li><input id="MarginType-0" name="""+idx+"""MarginType type="radio" value="ISOLATED"> <label for="MarginType-0">ISOLATED</label></li><li><input id="MarginType-1" name=""" + \
            idx+"""MarginType type="radio" value="CROSSED" checked> <label for="MarginType-1">CROSSED</label></li></ul>"""

    else:
        MarginType_ = """<ul onChange="add_text(this.id)" id="""+idx+"""MarginType><li><input id="MarginType-0" name="""+idx+"""MarginType type="radio" value="ISOLATED"> <label for="MarginType-0">ISOLATED</label></li><li><input id="MarginType-1" name=""" + \
            idx+"""MarginType type="radio" value="CROSSED"> <label for="MarginType-1">CROSSED</label></li></ul>"""

    if ReOpenOrder == "ON":

        ReOpenOrder_ = """<ul onChange="add_text(this.id)" id="""+idx+"""ReOpenOrder ><li><input id="ReOpenOrder-0" name="""+idx+"""ReOpenOrder type="radio" value="ON" checked> <label for="ReOpenOrder-0">ON</label></li><li><input id="ReOpenOrder-1" name=""" + \
            idx+"""ReOpenOrder type="radio" value="OFF"> <label for="ReOpenOrder-1">OFF</label></li></ul>"""
    elif ReOpenOrder == "OFF":
        ReOpenOrder_ = """<ul onChange="add_text(this.id)" id="""+idx+"""ReOpenOrder ><li><input id="ReOpenOrder-0" name="""+idx+"""ReOpenOrder  type="radio" value="ON"> <label for="ReOpenOrder-0">ON</label></li><li><input id="ReOpenOrder-1" name=""" + \
            idx+"""ReOpenOrder type="radio" value="OFF" checked> <label for="ReOpenOrder-1">OFF</label></li></ul>"""

    else:
        ReOpenOrder_ = """<ul onChange="add_text(this.id)" id="""+idx+"""ReOpenOrder><li><input id="ReOpenOrder-0" name="""+idx+"""ReOpenOrder type="radio"  value="ON"> <label for="ReOpenOrder-0">ON</label></li><li><input id="ReOpenOrder-1" name=""" + \
            idx+"""ReOpenOrder  type="radio" value="OFF"> <label for="ReOpenOrder-1">OFF</label></li></ul>"""

    if type_ == "Future":
        future_option = """ <div class="input-group m-2">
                                                    <div class="col">
                                                        <div class="row">
                                                            <div class="col">
                                                                MarginType 
                                                                """+MarginType_+"""
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="col">
                                                        <div class="row">
                                                            <div class="col">
                                                                ReOpenOrder 
                                                                 """+ReOpenOrder_+"""
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>"""
    else:
        future_option = ""

    html_modal = """<div class="modal fade" id="detail_Bot_"""+id+"""modal" tabindex="-1" aria-labelledby="detail_Bot_"""+id+"""_Label" aria-hidden="true">
                                <div class="modal-dialog modal-dialog-centered">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title" id="detail_Bot_"""+id+"""_Label">Detail</h5>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body">
                                            
                                            <form>
                                                """+future_option+"""
                                                <div class="row">
                                                    <div class="input-group m-2">
                                                        <span class="input-group-text">Label API</span> <input class="form-control" id="""+idx+"""Label_API name="Label_API" type="tel" onChange="add_text(this.id)" value='"""+str(Label_API)+"""' > 
                                                    </div>
                                                    <div class="input-group m-2">
                                                        <span class="input-group-text">API Key</span> <input class="form-control" id="""+idx+"""API_Key name="API_Key" type="tel" onChange="add_text(this.id)" value="""+API_Key+"""> 
                                                    </div>
                                                    <div class="input-group m-2">
                                                        <span class="input-group-text">API SECRET</span> <input class="form-control" id="""+idx+"""API_SECRET name="API_SECRET" onChange="add_text(this.id)" type="tel" value="""+API_SECRET+"""> 
                                                    </div>
                                                    <div class="input-group m-2">
                                                        <span class="input-group-text">LineNotify</span> <input class="form-control" id="""+idx+"""LineNotify name="LineNotify" onChange="add_text(this.id)" type="tel" value="""+LineNotify+"""> 
                                                    </div>
                                                    <div class="input-group m-2">
                                                        <span class="input-group-text">PassPhrase</span> <input class="form-control" id="""+idx+"""PassPhrase name="PassPhrase" onChange="add_text(this.id)" type="tel" value="""+PassPhrase+"""> 
                                                    </div>
                                                </div>
                                            </form>
                                        </div>
                                        <div class="modal-footer">
                                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                            <input class="btn btn-primary" id="api_update" name="api_update" type="submit" value="api_update">
                                        </div>
                                    </div>
                                </div>
                            </div>"""

    return html_modal
