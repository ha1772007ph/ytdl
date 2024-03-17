import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import subprocess
import json

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
def getq(url):
    q=[]
    command = ["yt-dlp", "-F", url]
    
    try:
        # Capture the output of the command
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
        # Check for errors
        result.check_returncode()
        # Get the download URL from the output (assuming it's on the first line)
        for qline in result.stdout.splitlines()[8:]:
            qls = qline.split(None, 1)
            # print(qls[0])
            q.append({})
            q[len(q)-1]['id'] = qline[:8].strip().replace('[', '<b>').replace(',','<q>')
            q[len(q)-1]['ext'] = qline[8:14].strip().replace('[', '<b>').replace(',','<q>')
            q[len(q)-1]['resolution'] = qline[14:25].strip().replace('[', '<b>').replace(',','<q>')
            # q[len(q)-1]['fps'] = qline[25:30].strip().replace('[', '<b>').replace(',','<q>')
            # q[len(q)-1]['ch'] = qline[30:32].strip().replace('[', '<b>').replace(',','<q>')
            q[len(q)-1]['filesize'] = qline[33:44].strip().replace('[', '<b>').replace(',','<q>')
            # q[len(q)-1]['tbr'] = qline[47:51].strip().replace('[', '<b>').replace(',','<q>')
            q[len(q)-1]['proto'] = qline[51:57].strip().replace('[', '<b>').replace(',','<q>')
            q[len(q)-1]['vcodec'] = qline[60:75].strip().replace('[', '<b>').replace(',','<q>')
            # q[len(q)-1]['vbr'] = qline[71:78].strip().replace('[', '<b>').replace(',','<q>')
            q[len(q)-1]['acodec'] = qline[81:91].strip().replace('[', '<b>').replace(',','<q>')
            # q[len(q)-1]['abr'] = qline[87:91].strip().replace('[', '<b>').replace(',','<q>')
            # q[len(q)-1]['ask'] = qline[91:95].strip().replace('[', '<b>').replace(',','<q>')
            # q[len(q)-1]['more'] = qline[95:100].strip()
            # q[len(q)-1]['info'] = qline[100:].strip().replace('[', '<b>').replace(',','<q>')
    except subprocess.CalledProcessError:
        print("Error: Failed to get download URL for", url)
        return None
    return q
def gu(id,url):
    try:
        command = ["yt-dlp","--get-url","-f",id, url]

        # Capture the output of the command
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
        # Check for errors
        result.check_returncode()
        # Get the download URL from the output (assuming it's on the first line)
        return result.stdout
        # return command
        # return result.stdout
    except subprocess.CalledProcessError:
        return 'Could not get URL'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def yt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if  len(update.message.text.split(' ')) == 2:
        byuser1 = update.message.text.split(' ')[1]
        qrec = getq(byuser1)
        qrecmf = ''
        for qrecm in  qrec:
            qrecmf = qrecmf + ' ID: ' + qrecm['id'] + ' EXT: ' + qrecm['ext'] + ' RES: ' + qrecm['resolution'] + ' FS: ' + qrecm['filesize'] + ' PROTO: '+ qrecm['proto'] + ' VC: '+ qrecm['vcodec'] + ' AC: '+ qrecm['acodec'] + '\n'
        nq = len(qrecmf.splitlines()) // 20
        nqrecmf = 0
        while nqrecmf < nq:
            ssqrecmf = 20 * nqrecmf
            if((nqrecmf + 1) == nq):
                esqrecmf = len(qrecmf.splitlines(keepends=True))
            else:
                esqrecmf = 20 * (nqrecmf + 1)
            sqrecmf =  qrecmf.splitlines()[ssqrecmf:esqrecmf]
            sendingtext = '\n\n'.join(sqrecmf)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=sendingtext)
            nqrecmf+=1
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Invalid command Given')
async def geturl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gu1 = update.message.text.split(' ')[1]
    gu2 = update.message.text.split(' ')[2]
    gumessage = gu(gu1,gu2)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=gumessage)


if __name__ == '__main__':
    application = ApplicationBuilder().token('6738580545:AAGb5e860lIMsm-HoIy7krvkfTbOSqMZIxg').build()  # Replace with your actual bot token

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    yt_handler = CommandHandler('yt', yt)
    application.add_handler(yt_handler)
    geturl_handler = CommandHandler('geturl', geturl)
    application.add_handler(geturl_handler)

    application.run_polling()
