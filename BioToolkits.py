import pynecone as pc
from styles import *
from utils import maketd,format_output,makeOut,navbar
from states import State,Sequence,Excel2shell



def index()->pc.components:
    return pc.vstack(
        navbar(),
        pc.center(
        pc.vstack(
            pc.heading("Introduction:"),
            pc.text("This is a web toolkits build by xiaoguang!"),
        ),
            style=index_body_style,
            ),
            spacing="0em",
            fontFamily="Open Sans",
    )

def seuquencetools()->pc.components:
    return pc.vstack(
                navbar(),
                pc.center(
                pc.circle(style=[circle_style,circle1_style]),
                pc.circle(style=[circle_style,circle2_style]),
                pc.center(
                    pc.vstack(
                        pc.heading("Seq tools!",style=heading_style),
                        pc.box(pc.heading("Introduction:",size="md"),
                               pc.text("""Welcome to Seqtools! It's a Pynecone-based tool for processing genomic sequences.featuring reverse complementation and translation. Its most notable functionality
                                        includes the ability to retrieve input sequence positions on the reference genome via UCSC's BLAT interface. 
                                        Currently limited to human-genome support only, this tool accurately locates genomic data with ease.
                                        """),
                        pc.heading("Usage: ",size="md"),
                        pc.text("You should input a format like fasta files: "),
                        pc.text(">1"),
                        pc.text("TGTTCGGCAAGATCTCGGGCTGG"),
                        pc.text(">2"),
                        pc.text("AACAATGATCGCCCGAGTGGCGG"),
                              ),
                        pc.text_area(value=Sequence.input,
                                    placeholder="Input your seq...",
                                    on_change = Sequence.set_input,
                                    on_blur = Sequence.change_dis,
                                    width="100%",
                                    borderWidth="medium",
                                    borderColor="#bdbdbd"),
                        pc.hstack(pc.button("Complement!",
                                            on_click = Sequence.complement,
                                            style=button_style,
                                            is_disabled= Sequence.dis),
                                  pc.button("Reverse Comp!",
                                            on_click = Sequence.rev_complement,
                                            style=button_style,
                                            is_disabled=Sequence.dis),
                                  pc.button("Translate!",
                                            on_click = Sequence.translate,
                                            style=button_style,
                                            is_disabled=Sequence.dis),
                                ),
                        pc.hstack(pc.button("Blat!",
                                            style=button_style,
                                            on_click = [Sequence.nima,Sequence.blat],
                                            is_disabled= Sequence.dis),
                                  pc.button("Clean!",
                                            style=button_style,
                                            on_click = Sequence.clean
                                            )
                                  
                                ),
                        pc.divider(),
                        pc.alert_dialog(
                            pc.alert_dialog_overlay(
                                pc.alert_dialog_content(
                                    pc.alert_dialog_header("Info"),
                                    pc.alert_dialog_body(
                                            "No BLAT matches were found for this sequence in genome"
                                                            ),
                                    pc.alert_dialog_footer(
                                    pc.button(
                                            "Close",
                                            on_click=Sequence.change,
                                            )
                                                            ),
                                                        )
                                                    ),
                                    is_open=Sequence.show,
                                        ),
                        pc.box(
                            pc.foreach(Sequence.output,format_output),
                            style=seq_style
                              ),
                        pc.divider(),
                        pc.cond(
                            Sequence.waiting,
                            pc.html("</hr>"),
                            pc.circular_progress(is_indeterminate=True)),
                            pc.table_container(
                                pc.table(
                                    pc.thead(
                                        pc.tr(
                                            pc.th("Name"),
                                            pc.th("Chrom"),
                                            pc.th("Start"),
                                            pc.th("End"),
                                            pc.th("Strand")
                                            )
                                            ),
                                    pc.tbody(pc.foreach(Sequence.blatData,maketd)))),
                    ),
                style = body_style),
    style=all_style,
    ),
    spacing="0em",
    )
            

def excel2shell() -> pc.Component:
    return pc.box(
        navbar(),
        pc.vstack(
            pc.heading("Excel2Shell",font_family="Open Sans",),
            pc.flex(
                pc.vstack(
                    pc.text("Excel from Glims..."),
                    pc.hstack(
                            pc.button(
                                pc.icon(tag="attachment"),
                                "Attach..",
                                width="23%",
                                bgColor="#BBD1EA",
                                on_click = lambda: Excel2shell.handle_upload(pc.upload_files())
                    ),
                    pc.upload(
                            pc.box(
                                pc.text(Excel2shell.excel_file),
                                borderWidth="0.1px",
                                height="40px",
                                rounded="md",
                                spacing="0em",
                                borderColor="#f2ad85"
                        
                    ),
                        width="77%"), 
                    spacing="0em"
                    ),
                    pc.text("Index for sampleName:"),
                    pc.number_input(default_value=4,on_change=Excel2shell.set_sampleNameIndex,borderColor="#f2ad85"),
                    pc.text("Index for barcode:"),
                    pc.number_input(default_value=23,on_change=Excel2shell.set_barcodeIndex,borderColor="#f2ad85"),
                    pc.text("Index for chip:"),
                    pc.number_input(default_value=27,on_change=Excel2shell.set_chipIndex,borderColor="#f2ad85"),
                    pc.text("Index for lane:"),
                    pc.number_input(default_value=28,on_change=Excel2shell.set_laneIndex,borderColor="#f2ad85"),
                    pc.text("Index for dataPath:"),
                    pc.number_input(default_value=48,on_change=Excel2shell.set_datapathIndex,borderColor="#f2ad85"),
                    pc.text("Remote path:"),
                    pc.input(default_value="10.2.100.1:/pakpox/pob8d1",on_change=Excel2shell.set_remotePath,borderColor="#f2ad85"),
                    pc.hstack(
                        pc.button(
                            pc.icon(tag="search"),
                            "Submit!",
                            on_click=Excel2shell.getCmd,
                            bgColor="#F7CAC9",
                            width="23%",
                                ),
                        pc.button(
                            "View data",
                            width="23%",
                            bgColor="#92DCE5",
                            on_click=Excel2shell.change,),
                        pc.modal(
                            pc.modal_overlay(
                            pc.modal_content(
                                pc.modal_header("Confirm"),
                                    pc.modal_body(
                                        pc.data_table(data=Excel2shell.modalData,pagination=True,
                                                      search=True,
                                                      sort=True,),
                                        ),
                            pc.modal_footer(
                                    pc.button(
                                        "Close", on_click=Excel2shell.change
                                        )
                                            ),
                                                )
                                                ),
                            is_open=Excel2shell.show2,
                            size="6xl",
                            return_focus_on_close=True
                            ),
                    ),
                    pc.divider(
                        borderWidth="0.5px",
                        borderColor="black"
                    ),
                    pc.text("Input Barcode with sampleName:"),
                    pc.hstack(
                            pc.button(
                                pc.icon(tag="attachment"),
                                "Attach..",
                                width="23%",
                                #height="40px",
                                bgColor="#BBD1EA",
                                on_click = lambda: Excel2shell.handle_upload2(pc.upload_files())
                    ),
                    pc.upload(
                            pc.box(
                                pc.text(Excel2shell.barcode_file),
                                borderWidth="0.1px",
                                height="40px",
                                rounded="md",
                                spacing="0em",
                                borderColor="#f2ad85"
                        
                    ),
                        width="77%"), 
                    spacing="0em"
                    ),
                    pc.button(pc.icon(tag="repeat"),
                            "Update!",
                            on_click=Excel2shell.removename,
                            bgColor="#F7CAC9",
                            width="23%",),
                    style=excel_body_style,),
                pc.spacer(),
                pc.vstack(
                    pc.heading("Shell Script",size="md",font_family="Open Sans",),
                    pc.divider(borderWidth="0.5px",),
                    pc.tabs(
                        items=[
                            ("Script 1", pc.box(pc.foreach(Excel2shell.cmd1,makeOut),
                                                            overflow="scroll",
                                                            maxH="600px",
                                                            minH="600px")),
                            ("Script 2", pc.box(pc.foreach(Excel2shell.cmd2,makeOut),
                                                            overflow="scroll",
                                                            maxH="600px",
                                                            minH="600px")),
                                ],
                        ),
                    style=excel_textOut_style,
            ),
            width="80%",
            
       ),
            bgColor="#DFE9F2",
            padding="1.5%",
            font_family="Open Sans",
        ),
        )
    
    
app = pc.App(state=State,stylesheets=[
        "https://fonts.googleapis.com/css2?family=Open+Sans&display=swap",
    ],)
app.add_page(index,title="Xiaoguang's Toolkits")
app.add_page(seuquencetools,title="Xiaoguang's Toolkits")
app.add_page(excel2shell,title="Xiaoguang's Toolkits")
app.compile()