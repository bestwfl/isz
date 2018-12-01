import traceback

from common.base import consoleLog

try:
    int('ad')
except Exception as e:
    print traceback.format_exc()
    consoleLog(e.args, 'e')