from bs4 import BeautifulSoup


def table_to_json(html):
    table_data = [
        [cell.text for cell in row("td")] for row in BeautifulSoup(html)("tr")
    ]
    return dict(table_data)


def extract_tables_from_html(html):
    soup = BeautifulSoup(html)
    print(soup.prettify())
    # htag = soup.findall('h4')
    # tabletag = soup.findall('table')
    # for h in htag:
    #     print(h.text)
    # for table in tabletag:
    #     print(table.text)


def extract_tables_from_html_pandas(html: str):
    import pandas as pd

    dfs = pd.read_html(html)
    return dfs


if __name__ == "__main__":
    html_data = """
    <table>
    <tr>
        <td>Card balance</td>
        <td>$18.30</td>
    </tr>
    <tr>
        <td>Card name</td>
        <td>NAME</td>
    </tr>
    <tr>
        <td>Account holder</td>
        <td>NAME</td>
    </tr>
    <tr>
        <td>Card number</td>
        <td>1234</td>
    </tr>
    <tr>
        <td>Status</td>
        <td>Active</td>
    </tr>
    </table>
    """
    dct = table_to_json(html_data)
    print(dct)

    extract_tables_from_html(html_data)

    html_data = """          <table border="0" cellpadding="0" cellspacing="0" width="100%">
           <tbody>
            <!-- start: travel summary -->
            <tr>
             <td class="module" valign="top">
              <table border="0" cellpadding="0" cellspacing="0" id="travelSummary" width="100%">
               <tbody>
                <tr>
                 <td class="container" style="padding-bottom: 10px;" valign="top">
                  <table class="background" style="background-color: #FFFFFF;" valign="top" width="100%">
                   <tbody>
                    <!-- start: row-1 (flight summary) -->
                    <tr class="row-1">
                     <td style="padding: 15px;" valign="top">
                      <table border="0" cellpadding="0" cellspacing="0" style="border-bottom: 1px solid #CCCCCC;" width="100%">
                       <tbody>
                        <tr>
                         <!-- left column -->
                         <th class="split" style="padding: 0; font-weight: normal;" valign="top">
                          <table border="0" cellpadding="0" cellspacing="0" class="column left" width="454">
                           <tbody>
                            <tr>
                             <td style="padding-bottom: 5px;" valign="top">
                              <p style="color: #646464; font-size: 14px; font-weight: bold; font-family: Arial, Helvetica, 'sans-serif'; text-align: left; Margin: 0;">
                               June 27
                              </p>
                             </td>
                            </tr>
                            <tr>
                             <td style="padding-bottom: 10px;" valign="top">
                              <table align="left" border="0" cellpadding="0" cellspacing="0">
                               <tbody>
                                <tr>
                                 <td valign="middle">
                                  <p style="color: #111B40; font-size: 40px; font-family: Arial, Helvetica, 'sans-serif'; text-align: left; Margin: 0;">
                                   SEA
                                  </p>
                                 </td>
                                 <td style="padding: 0 10px;" valign="middle">
                                  <img alt="" border="0" src="https://res.iluv.southwest.com/res/southwe_mkt_prod1/ico-plane.png" style="display: block;" width="27"/>
                                 </td>
                                 <td valign="middle">
                                  <p style="color: #111B40; font-size: 40px; font-family: Arial, Helvetica, 'sans-serif'; text-align: left; Margin: 0;">
                                   OAK
                                  </p>
                                 </td>
                                </tr>
                               </tbody>
                              </table>
                             </td>
                            </tr>
                            <tr>
                             <td style="padding-bottom: 15px;" valign="top">
                              <p style="color: #646464; font-size: 16px; font-family: Arial, Helvetica, 'sans-serif'; text-align: left; Margin: 0;">
                               Seattle/Tacoma to Oakland
                              </p>
                             </td>
                            </tr>
                           </tbody>
                          </table>
                         </th>
                         <!-- right column -->
                         <th class="split" style="padding: 0; font-weight: normal;" valign="top">
                          <table border="0" cellpadding="0" cellspacing="0" class="column right" width="101">
                           <tbody>
                            <tr>
                             <td align="top" class="btn-wrap" style="padding-bottom: 15px;">
                              <table border="0" cellpadding="0" cellspacing="0" style="border: 1px solid #CCCCCC; border-radius: 2px; -ms-border-radius: 2px; -webkit-border-radius: 2px;">
                               <tbody>
                                <tr>
                                 <td class="btn" height="33" valign="middle" width="100">
                                  <p style="color: #304CB2; font-size: 14px; font-weight: bold; font-family: Arial, Helvetica, 'sans-serif'; text-align: center; Margin: 0;">
                                   <a _label="TravelSummary_Itinerary" href="https://t.iluv.southwest.com/r/?id=h6e31cf23,135cba1f,11e1db7b&amp;RR_NUMBER=b6589fc6ab0dc82cf12099d1c2d40ab994e8410c&amp;RSD=0000&amp;RMID=AC_Pretrip_1Day&amp;RRID=cbc38468fb237b50730b39b4e8ac95ded57c769e6a9e83471b4c3864d6c82af2&amp;src=MAILTXNPRET1DAYDO200510&amp;p1=2C447Z&amp;p2=Brendan" style="color: #304CB2; text-decoration: none;">
                                    Full itinerary
                                   </a>
                                  </p>
                                 </td>
                                </tr>
                               </tbody>
                              </table>
                             </td>
                            </tr>
                           </tbody>
                          </table>
                         </th>
                        </tr>
                       </tbody>
                      </table>
                     </td>
                    </tr>
                    <!-- end: row-1 (flight summary) -->
                    <!-- start: row-2 (passenger summary) -->
                    <tr class="row-2">
                     <td style="padding: 0 15px;" valign="top">
                      <table border="0" cellpadding="0" cellspacing="0" width="100%">
                       <tbody>
                        <tr>
                         <td style="padding-bottom: 15px;" valign="top">
                          <p style="color: #111B40; font-size: 14px; font-family: Arial, Helvetica, 'sans-serif'; text-align: left; Margin: 0 0 3px 0;">
                           Confirmation #
                           <span style="color: #008522; font-size: 32px;">
                            <strong>
                             2C447Z
                            </strong>
                           </span>
                          </p>
                          <p style="color: #646464; font-size: 14px; font-weight: bold; font-family: Arial, Helvetica, 'sans-serif'; text-align: left; Margin: 0 0 3px 0;">
                           PASSENGER
                          </p>
                          <p style="color: #111B40; font-size: 14px; font-weight: bold; font-family: Arial, Helvetica, 'sans-serif'; text-align: left; Margin: 0 0 3px 0;">
                           Brendan Fortuner
                          </p>
                         </td>
                        </tr>
                       </tbody>
                      </table>
                     </td>
                    </tr>
                    <!-- end: row-2 (passenger summary) -->
                   </tbody>
                  </table>
                 </td>
                </tr>
               </tbody>
              </table>
             </td>
            </tr>
            <!-- end: travel summary -->
            <!-- start: itinerary -->
            <tr>
             <td class="container" style="padding-bottom: 10px;" valign="top">
              <p style="color: #111B40; font-size: 22px; font-weight: bold; font-family: Arial, Helvetica, 'sans-serif'; text-align: left; Margin: 0;">
               Your complete itinerary
              </p>
             </td>
            </tr>
            <tr>
             <td class="container" id="itinerary" style="padding-bottom: 10px;" valign="top">
              <table border="0" cellpadding="0" cellspacing="0" class="background" style="background-color: #FFFFFF;" width="100%">
               <tbody>
                <tr>
                 <td class="head" valign="top">
                  <table border="0" cellpadding="0" cellspacing="0" style="background-color: #111B3F;" width="100%">
                   <tbody>
                    <tr>
                     <td style="padding: 5px 15px;" valign="top">
                      <p style="color: #FFFFFF; font-size: 13px; font-family: Arial, Helvetica, sans-serif; text-align: left; Margin: 0;">
                       <strong>
                        Flight :
                       </strong>
                       Sunday 06/27/2021
                      </p>
                     </td>
                    </tr>
                   </tbody>
                  </table>
                 </td>
                </tr>
                <tr>
                 <td class="ond" style="padding: 15px;" valign="top">
                  <table border="0" cellpadding="0" cellspacing="0" width="100%">
                   <tbody>
                    <tr>
                     <td class="seg" valign="top">
                      <table border="0" cellpadding="0" cellspacing="0" width="100%">
                       <tbody>
                        <tr>
                         <th class="split" style="padding: 0; font-weight: normal;" valign="middle">
                          <table border="0" cellpadding="0" cellspacing="0" class="column left" width="75">
                           <tbody>
                            <tr>
                             <td style="padding-right: 20px;" valign="middle">
                              <p style="color: #111B40; font-size: 13px; font-family: Arial, Helvetica, sans-serif; text-align: left; Margin: 0;">
                               FLIGHT
                              </p>
                              <p style="color: #111B40; font-size: 13px; font-weight: bold; font-family: Arial, Helvetica, sans-serif; text-align: left; Margin: 0;">
                               # 4770
                              </p>
                             </td>
                            </tr>
                           </tbody>
                          </table>
                         </th>
                         <th class="split" style="padding: 0; font-weight: normal;" valign="middle">
                          <table border="0" cellpadding="0" cellspacing="0" class="column right" width="495">
                           <tbody>
                            <tr>
                             <td valign="top" width="140">
                              <p style="color: #636363; font-size: 13px; font-weight: bold; font-family: Arial, Helvetica, sans-serif; text-align: left; Margin: 0 0 5px 0;">
                               DEPARTS
                              </p>
                              <p style="color: #13247C; font-size: 13px; font-family: Arial, Helvetica, sans-serif; text-align: left; Margin: 0 0 3px 0;">
                               <span style="font-size: 18px;">
                                <strong>
                                 SEA 7:35
                                </strong>
                               </span>
                               PM
                              </p>
                              <p style="color: #636363; font-size: 13px; font-family: Arial, Helvetica, sans-serif; text-align: left; Margin: 0;">
                               Seattle/Tacoma
                              </p>
                             </td>
                             <td class="hide" style="padding: 0 20px;" valign="middle">
                              <img alt="" border="0" src="https://res.iluv.southwest.com/res/southwe_mkt_prod1/ico-plane.png" style="display: block;" width="27"/>
                             </td>
                             <td valign="top">
                              <p style="color: #636363; font-size: 13px; font-weight: bold; font-family: Arial, Helvetica, sans-serif; text-align: left; Margin: 0 0 5px 0;">
                               ARRIVES
                              </p>
                              <p style="color: #13247C; font-size: 13px; font-family: Arial, Helvetica, sans-serif; text-align: left; Margin: 0 0 3px 0;">
                               <span style="font-size: 18px;">
                                <strong>
                                 OAK 9:45
                                </strong>
                               </span>
                               PM
                              </p>
                              <p style="color: #636363; font-size: 13px; font-family: Arial, Helvetica, sans-serif; text-align: left; Margin: 0;">
                               Oakland
                              </p>
                             </td>
                            </tr>
                           </tbody>
                          </table>
                         </th>
                        </tr>
                       </tbody>
                      </table>
                     </td>
                    </tr>
                   </tbody>
                  </table>
                 </td>
                </tr>
               </tbody>
              </table>
             </td>
            </tr>
            <!-- end: itinerary -->
           </tbody>
          </table>"""
    dct = table_to_json(html_data)
    print(dct)
