from lollangCompiler.compiler import Compiler
from google.cloud import storage
import io
import json
import time

printLog=[]

def main(request):
    global printLog
    printLog = []
    
    output=''
    rawPyFile=[]
    pyFile=[]

    COMPILER_VERSION = 'v1.1'
    RES_TYPE = {
        "ERROR" : "ERROR",
        "SUCCESS" : "SUCCESS"
    }
    
    try:
        headers = {
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Allow-Origin': '*'
        }

        # 요청 수신부
        reqJson = request.get_json(force=True)
        code = ''
        if reqJson and 'message' in reqJson:
            code = reqJson['message']
        else:
            raise Exception('*.lo코드가 서버로 정상적으로 전달되지 않았습니다.')

        # lo파일 -> py파일 컴파일
        rawPyFile = compileLoFile(code)
        print('rawPyFile', str(rawPyFile))

        # 컴파일된 원천 py파일 후처리
        pyFile = postProcessPyFile(rawPyFile)
        print('pyFile', str(pyFile))

        # 후처리된 py파일 실행
        output = runPyFile(pyFile)
        print('output', output)
        
        # 모든 절차 성공 후 프론트엔드로 결과 반환
        res = {
            "resType" : RES_TYPE['SUCCESS'],
            "compilerVersion" : COMPILER_VERSION,
            "requestCode" : code,
            "result" : output,
            "pythonCode_raw" : rawPyFile,
            "pythonCode_postprocessed" : pyFile
        }
        resStr = json.dumps(res, ensure_ascii=False)
        return (resStr, 200, headers)

    except Exception as err:
        print('main except', err)
        res = {
            "resType" : RES_TYPE['ERROR'],
            "compilerVersion" : COMPILER_VERSION,
            "requestCode" : code,
            "result" : str(err),
            "pythonCode_raw" : rawPyFile,
            "pythonCode_postprocessed" : pyFile
        }
        resStr = json.dumps(res, ensure_ascii=False)
        print('main except resStr', resStr)
        return (resStr, 200, headers)

def compileLoFile(code):
    codelines = code.split('\n')
    cmp = Compiler()

    try :
        cmp.compile(codelines)
        print(cmp.out)
        return cmp.out[:]
    except TypeError:
        raise Exception(f"{cmp.currentLine}번째 적이 학살중입니다!!")
    except SyntaxError:
        raise Exception(f"{cmp.currentLine}번째 적은 전설적입니다!!")
    except ValueError:
        raise Exception(f"{cmp.currentLine}번째 적을 도저히 막을 수 없습니다!!")
    except KeyError:
        raise Exception(f"{cmp.currentLine}번째 적이 전장을 지배하고 있습니다!!")
    
    except FileNotFoundError:
        raise Exception("서버에 연결할 수 없습니다.")


def postProcessPyFile(rawPyFile):
    pyFile=rawPyFile[:]
    for i in range(len(pyFile)):
        if "print()" in pyFile[i]:
            pyFile[i] = pyFile[i].replace('print()', "printLog.append('\\n')")
        else:  
          if 'print(' in pyFile[i] and 'print()' not in pyFile[i]:
                pyFile[i] = pyFile[i].replace('print(', 'printLog.extend([')
          if ",end='')" in pyFile[i]:
              pyFile[i] = pyFile[i].replace(",end='')", "])")
    
    return pyFile


def runPyFile(pyFile):
    try:
        # printLog=[]  <--- 코드 가장 윗부분에 전역변수로 선언됨
        exec('\n'.join(pyFile))
        
        for i in range(len(printLog)):
            if type(printLog[i]) is not str:
                printLog[i] = str(printLog[i])
        
        output = ''.join(printLog)
        return output
    except ZeroDivisionError:
        raise Exception("적이 전장의 화신입니다!!")
    except Exception as ex:
        print(ex)
        raise Exception("소환사 한명이 게임을 종료했습니다.")