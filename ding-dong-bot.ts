import 'dotenv/config.js'

import {
  Contact,
  Message,
  ScanStatus,
  WechatyBuilder,
  log,
}                  from 'wechaty'

import qrcodeTerminal from 'qrcode-terminal'

function onScan (qrcode: string, status: ScanStatus) {
  if (status === ScanStatus.Waiting || status === ScanStatus.Timeout) {
    const qrcodeImageUrl = [
      'https://wechaty.js.org/qrcode/',
      encodeURIComponent(qrcode),
    ].join('')
    log.info('StarterBot', 'onScan: %s(%s) - %s', ScanStatus[status], status, qrcodeImageUrl)

    qrcodeTerminal.generate(qrcode, { small: true })  // show qrcode on console

  } else {
    log.info('StarterBot', 'onScan: %s(%s)', ScanStatus[status], status)
  }
}

function onLogin (user: Contact) {
  log.info('StarterBot', '%s login', user)
}

function onLogout (user: Contact) {
  log.info('StarterBot', '%s logout', user)
}

async function postData(url: string) {
  const response = await fetch(url, {
    method: 'GET',
  });
  return response.json(); // 解析响应数据为 JSON 格式
}

// 调用函数并处理返回的 Promise


async function onMessage (msg: Message) {
  log.info('StarterBot', msg.toString())

  if (msg.text() === '开灯') {
    await msg.say('灯光已经开启')
    postData('http://192.168.137.189/pin?light=on')
  }
  if (msg.text() === '关灯') {
    await msg.say('灯光已经关闭')
    postData('http://192.168.137.189/pin?light=off')
  }
  
}

const bot = WechatyBuilder.build({
  name: 'ding-dong-bot',
})

bot.on('scan',    onScan)
bot.on('login',   onLogin)
bot.on('logout',  onLogout)
bot.on('message', onMessage)

bot.start()
  .then(() => log.info('StarterBot', 'Starter Bot Started.'))
  .catch(e => log.error('StarterBot', e))
