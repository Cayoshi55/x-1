

from email import message
from turtle import color


def html_isbot(id_bot, type_bot, datetime, Label_API, status):

    date_time = datetime

    id = ""
    id = str(id_bot)
    type_ = str(type_bot)
    if status == "stop":
        ids = "pause_bot_"+id
        color = "bg-secondary bg-gradient"
        message_ = " data-bs-mess_title='Bot Start' data-bs-mess_body='Are you sure Start ?' "
    else:
        ids = "running_bot_"+id
        color = "bg-success bg-gradient"
        message_ = " data-bs-mess_title='Bot Pause' data-bs-mess_body='Are you sure Pause ?' "
    if str(status) == "stop":
        icon = "bell"
    else:
        icon = "bell-off"
    if type_ == "Future":
        on_click = """onClick="reply_click_future(this.id)"""
        future_option = """  <div class="mb-0">
                                                <div>
                                                    <span class="text-success" >
                                                    Long alert: 59
                                                    Close Long : 59
                                                    </span>
                                                </div>

                                                <div >
                                                    <span class="text-danger">
                                                    Short alert: 58
                                                    Close Short : 58
                                                    </span>
                                                </div>

                                                <div><span class="text-muted">Start date: """+str(date_time) + """</span></div>
                                            </div>"""
    else:
        on_click = """onClick="reply_click_spot(this.id)"""
        future_option = """  <div class="mb-0">
                                                <div>
                                                    <span class="text-success">
                                                    Buy alert: 59
                                                     </span>
                                                </div>

                                                <div>
                                                     <span class="text-danger">           
                                                    Sell alert: 58
                                                     </span>
                                                </div>

                                                <div><span class="text-muted">Start date: """+str(date_time) + """</span></div>
                                            </div>"""
    html2 = """ <div class="col">
                                    <div class="card bg-dark" style="border-radius: 1rem">
                                        <div class="card-body">
                                            <div class="row">
                                                <nav class="navbar navbar-light """+color+""" m-0 p-0" style="border-radius: 0.5rem">
                                                    <div class="container-fluid">
                                                        <a class="navbar-brand text-white">"""+str(Label_API) + """</a>
                                                        <form class="d-flex" method="POST">
                                                        <a class="nav-icon dropdown-toggle text-white" id="code_Bot_"""+id+"""" onClick="post_click(this.id)" data-bs-toggle="modal" data-bs-target="#code_Bot_"""+id+"""modal">
                                                                <div class="position-relative justify-content-md-end">
                                                                    <i class="align-middle mx-0" data-feather="code"></i>

                                                                </div>
                                                            </a>
                                                            <a class="nav-icon dropdown-toggle text-white" id="detail_Bot_"""+id+"""" """+on_click+"""" data-bs-toggle="modal" data-bs-target="#detail_Bot_"""+id+"""modal">
                                                                <div class="position-relative justify-content-md-end">
                                                                    <i class="align-middle mx-0" data-feather="help-circle"></i>

                                                                </div>
                                                            </a>

                                                            <a class="nav-icon dropdown-toggle text-white" id="""+ids+""" """+on_click+"""" data-bs-toggle="modal" data-bs-target="#pause_bot_Modal" """+message_+""">
                                                                <div class="position-relative justify-content-md-end">
                                                                    <i class="align-middle mx-0" data-feather="""+icon+""" ></i>

                                                                </div>
                                                            </a>



                                                            <a class="nav-icon dropdown-toggle text-white" id="delete_bot_"""+id+"""" """+on_click+"""" data-bs-toggle="modal" data-bs-target="#delete_bot_Modal">
                                                                <div class="position-relative justify-content-md-end">
                                                                    <i class="align-middle mx-0" data-feather="trash-2"></i>

                                                                </div>
                                                            </a>
                                                        </form>

                                                    </div>
                                                </nav>
                                            </div>

                                            <div class="row">

                                                <h3 class="mt-1 mb-3 text-white">"""+str(type_) + """</h3>

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
    #PassPhrase = '"'+str(PassPhrase)+'"'
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
        onChange = """onChange="add_text_future(this.id)"""
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
        onChange = """onChange="add_text_spot(this.id)"""
        future_option = ""

    html_modal = """<div class="modal fade" id="code_Bot_"""+id+"""modal" tabindex="-1" aria-labelledby="code_Bot_"""+id+"""_Label" aria-hidden="true">
                                <div class="modal-dialog modal-xl modal-dialog-centered">
                                    <div class="modal-content bg-dark bg-gradient text-light border-0">
                                        <div class="modal-header  text-light">
                                            <h5 class="modal-title  text-light" id="code_Bot_"""+id+"""_Label">Scrip</h5>
                                            <button type="button" class="btn-close bg-light text-light" data-bs-dismiss="modal" aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body">

                                            
                                               
                                                <div class="row">
                                                    <div class="input-group m-2">
                                                        <span class="input-group-text bg-dark bg-gradient text-light border border-dark">Scrip</span> <input class="form-control  bg-dark text-light border border-dark" id="""+idx+"""scrip name="scrip" type="tel" 
                                                     
                                                        value='{"side":"xxx","amount":"xxx","symbol":"xxx","passphrase":"""'"'+PassPhrase+'"'""","strategy":"xxx"}' >
                                                    </div>
                                                </div>
                                                <div class="row"><!-- copy_scrip hiden | d-none d-print-block | -->
                                                    <div class="col-md text-center d-none d-print-block">
                                                        <button type="button" class="btn btn-outline-primary bg-dark bg-gradient text-light border border-dark" id="""+idx+"""bt_scrip onClick="copy_scrip(this.id)"  >Copy</button>
                                                    </div> 
                                                </div>
                                                <!-- Modal -->
                                                <div class="row">
                                                    <div class="input-group m-2">
                                                        <span class="input-group-text   bg-dark bg-gradient text-light border border-dark">Test Send</span> <input class="form-control  bg-dark text-light border border-dark" id="""+idx+"""test_send name="""+idx+"""test_send type="tel" 
                                                        onChange="test_send(this.id)" 
                                                        value='{"side":"xxx","amount":"xxx","symbol":"xxx","passphrase":"""'"'+PassPhrase+'"'""","strategy":"xxx"}' >
                                                    </div>
                                                </div>
                                                  <div class="row">
                                                    <div class="col-md text-center">
                                                       
                                                        <input class="btn btn-dark border border-info" id="test_send" name="test_send" type="submit"  value="TEST SEND">
                                                    </div> 
                                                </div>
                                        </div>
                                        <div class="modal-footer border-0">
                                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                      
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="modal fade" id="detail_Bot_"""+id+"""modal" tabindex="-1" aria-labelledby="detail_Bot_"""+id+"""_Label" aria-hidden="true">
                                <div class="modal-dialog modal-dialog-centered">
                                    <div class="modal-content bg-dark bg-gradient text-light border-0">
                                        <div class="modal-header  border-0">
                                            <h5 class="modal-title text-light" id="detail_Bot_"""+id+"""_Label">Detail</h5>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body">

                                            <form>
                                                """+future_option+"""
                                                <div class="row">
                                                    <div class="input-group m-2">
                                                        <span class="input-group-text  bg-dark bg-gradient text-light border border-dark">Label API</span> <input class="form-control bg-dark text-light border border-dark" id="""+idx+"""Label_API name="Label_API" type="tel" """+onChange+"""" value='"""+str(Label_API)+"""' >
                                                    </div>
                                                    <div class="input-group m-2">
                                                        <span class="input-group-text  bg-dark bg-gradient text-light border border-dark">API Key</span> <input class="form-control bg-dark text-light border border-dark" id="""+idx+"""API_Key name="API_Key" type="tel" """+onChange+"""" value="""+API_Key+""">
                                                    </div>
                                                    <div class="input-group m-2">
                                                        <span class="input-group-text bg-dark bg-gradient text-light border border-dark">API SECRET</span> <input class="form-control bg-dark text-light border border-dark" id="""+idx+"""API_SECRET name="API_SECRET" """+onChange+"""" type="tel" value="""+API_SECRET+""">
                                                    </div>
                                                    <div class="input-group m-2">
                                                        <span class="input-group-text bg-dark bg-gradient text-light border border-dark">LineNotify</span> <input class="form-control bg-dark text-light border border-dark" id="""+idx+"""LineNotify name="LineNotify" """+onChange+"""" type="tel" value="""+LineNotify+""">
                                                    </div>
                                                    <div class="input-group m-2">
                                                        <span class="input-group-text bg-dark bg-gradient text-light border border-dark">PassPhrase</span> <input class="form-control bg-dark text-light border border-dark" id="""+idx+"""PassPhrase name="PassPhrase" """+onChange+"""" type="tel" value="""+PassPhrase+""" readonly>
                                                    </div>
                                                </div>
                                            </form>
                                        </div>
                                        <div class="modal-footer  border-0">
                                            <button type="button" class="btn btn-dark border border-info" data-bs-dismiss="modal">Close</button>
                                            <input class="btn btn-dark border border-info" id="api_update" name="api_update" type="submit" value="API UPDATE">
                                        </div>
                                    </div>
                                </div>
                            </div>"""

    return html_modal


def html_alert(date_timeA, label_api, bot_type, symbol, side, price, Quantity, amount, passphrase, strategy_name):

    htmls = """<tr>
                            <th class="d-none d-md-table-cell">"""+str(date_timeA)+"""</th>
                            <td class="d-none d-xl-table-cell">"""+str(label_api)+"""</td>
                            <td class="d-none d-xl-table-cell">"""+str(bot_type)+"""</td>
                            <th>"""+str(symbol)+"""</th>
                            <td><span class="alert-success">"""+str(side)+"""</span></td>
                            <td>"""+str(price)+"""</td>
                            <td class="d-none d-md-table-cell">"""+str(Quantity)+"""</td>
                            <td>"""+str(amount)+"""</td>
                            <td class="d-none d-md-table-cell">"""+str(passphrase)+"""</td>
                            <td class="d-none d-md-table-cell">"""+str(strategy_name)+"""</td>

                        </tr>"""

    return htmls
