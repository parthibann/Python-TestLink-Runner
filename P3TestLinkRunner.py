import unittest
import sys
import io
import xmlrpc

TestResult = unittest.TestResult

class _TestResult(TestResult):
    def __init__(self,_testLinkURL,_devKey,_testPlanId,_buildName):
        TestResult.__init__(self)
        self.stdout0 = None
        self.stderr0 = None
        self.result = []
        self.testLinkURL = _testLinkURL
        self.devKey = _devKey
        self.testPlanId = _testPlanId
        self.buildName = _buildName        
        
    def startTest(self, test):
        TestResult.startTest(self, test)
        # just one buffer for both stdout and stderr
        self.outputBuffer = io.StringIO()
        stdout_redirector.fp = self.outputBuffer
        stderr_redirector.fp = self.outputBuffer
        self.stdout0 = sys.stdout
        self.stderr0 = sys.stderr
        sys.stdout = stdout_redirector
        sys.stderr = stderr_redirector
        
    def complete_output(self):
        """
        Disconnect output redirection and return buffer.
        Safe to call multiple times.
        """
        if self.stdout0:
            sys.stdout = self.stdout0
            sys.stderr = self.stderr0
            self.stdout0 = None
            self.stderr0 = None
        return self.outputBuffer.getvalue()
    
    
    def stopTest(self, test):
        # Usually one of addSuccess, addError or addFailure would have been called.
        # But there are some path in unittest that would bypass this.
        # We must disconnect stdout in stopTest(), which is guaranteed to be called.
        self.complete_output()
        
    def addSuccess(self, test):
        TestResult.addSuccess(self, test)
        output = self.complete_output()
        self.result.append((0, test, output, ''))
        testNameInString = str(test)
        _testCaseApiId = self.getTestCaseId(testNameInString)
        _SuccessStatus = 'p'
        self.updateTestCaseResult(_testCaseApiId, _SuccessStatus)
                        
    def addError(self, test, err):
        TestResult.addError(self, test, err)
        _, _exc_str = self.errors[-1]
        output = self.complete_output()
        self.result.append((2, test, output, _exc_str))
        testNameInString= str(test)
        _testCaseApiId = self.getTestCaseId(testNameInString)
        _Errorstatus = 'f'
        _stackTrace = str(err)
        self.updateTestCaseResult(_testCaseApiId, _Errorstatus, _stackTrace)    
        
    def addFailure(self, test, err):
        TestResult.addFailure(self, test, err)
        _, _exc_str = self.failures[-1]
        output = self.complete_output()
        self.result.append((1, test, output, _exc_str))
        testNameInString= str(test)
        _testCaseApiId = self.getTestCaseId(testNameInString)
        _Failurestatus = 'f'
        _stackTrace = str(err)
        self.updateTestCaseResult(_testCaseApiId, _Failurestatus, _stackTrace)
        
    def getTestCaseId(self,fullTestName):
        testCaseName = fullTestName.split("(")[0]
        splitUntilTestId = testCaseName.split("_")[1]
        testCaseApiId = self.getDigits(splitUntilTestId)
        return testCaseApiId
        
    def getDigits(self,str):
        c = ""
        for i in str:
            if i.isdigit():
                c+=i
        return c
        
    def updateTestCaseResult(self,_testCaseApiId,_status,_notes=None):
        """
        """
        conn = xmlrpc.Server(self.testLinkURL)
        data = {}
        data["devKey"] = self.devKey
        data["testcaseid"] = _testCaseApiId
        data["testplanid"] = self.testPlanId
        data["buildname"] = self.buildName
        data["status"] = _status
        if _notes == None:
            _notes = 'Successful test does not contain notes'
        data["notes"] = _notes
        updateTestResult = conn.tl.reportTCResult(data) 
     
#------------------------------------------------------------------------
class TestLinkRunner():
    def __init__(self,_testLinkURL,_devKey,_testPlanId, _buildName):
        self.testLinkURL = _testLinkURL
        self.devKey = _devKey
        self.testPlanId = _testPlanId
        self.buildName = _buildName
        
    def run(self,test):
        result = _TestResult(self.testLinkURL,self.devKey,self.testPlanId,self.buildName)
        test(result)
        
#-------------------------------------------------------------------------        
class OutputRedirector(object):
    """ Wrapper to redirect stdout or stderr """
    def __init__(self, fp):
        self.fp = fp
 
    def write(self, s):
        self.fp.write(s)
 
    def writelines(self, lines):
        self.fp.writelines(lines)
 
    def flush(self):
        self.fp.flush()
 
stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)
#-- Import section
import unittest, sys, io, xmlrpc

#-- Global variables section
TestResult = unittest.TestResult

class _TestResult(TestResult):
    def __init__(self,_testLinkURL,_apiKey,_testPlanId,_buildName):
        TestResult.__init__(self)
        self.stdout0 = None
        self.stderr0 = None
        self.result = []
        self.testLinkURL = _testLinkURL
        self.devKey = _apiKey
        self.testPlanId = _testPlanId
        self.buildName = _buildName        
        
    def startTest(self, test):
        TestResult.startTest(self, test)
        # just one buffer for both stdout and stderr
        self.outputBuffer = io.StringIO()
        stdout_redirector.fp = self.outputBuffer
        stderr_redirector.fp = self.outputBuffer
        self.stdout0 = sys.stdout
        self.stderr0 = sys.stderr
        sys.stdout = stdout_redirector
        sys.stderr = stderr_redirector
        
    def complete_output(self):
        """
        Disconnect output redirection and return buffer.
        Safe to call multiple times.
        """
        if self.stdout0:
            sys.stdout = self.stdout0
            sys.stderr = self.stderr0
            self.stdout0 = None
            self.stderr0 = None
        return self.outputBuffer.getvalue()
    
    
    def stopTest(self, test):
        # Usually one of addSuccess, addError or addFailure would have been called.
        # But there are some path in unittest that would bypass this.
        # We must disconnect stdout in stopTest(), which is guaranteed to be called.
        self.complete_output()
        
    def addSuccess(self, test):
        TestResult.addSuccess(self, test)
        output = self.complete_output()
        self.result.append((0, test, output, ''))
        testNameInString = str(test)
        _testCaseApiId = self.getTestCaseId(testNameInString)
        self.updateTestCaseResult(_testCaseApiId, 'p',str(output))
                        
    def addError(self, test, err):
        TestResult.addError(self, test, err)
        _, _exc_str = self.errors[-1]
        output = self.complete_output()
        self.result.append((2, test, output, _exc_str))
        testNameInString= str(test)
        _testCaseApiId = self.getTestCaseId(testNameInString)
        self.updateTestCaseResult(_testCaseApiId, 'f', str(err))
        
    def addFailure(self, test, err):
        TestResult.addFailure(self, test, err)
        _, _exc_str = self.failures[-1]
        output = self.complete_output()
        self.result.append((1, test, output, _exc_str))
        testNameInString= str(test)
        _testCaseApiId = self.getTestCaseId(testNameInString)
        self.updateTestCaseResult(_testCaseApiId, 'f', str(err))
        
    def getTestCaseId(self,fullTestName):
        testCaseName = fullTestName.split("(")[0]
        splitUntilTestId = testCaseName.split("_")[1]
        testCaseApiId = self.getDigits(splitUntilTestId)
        return testCaseApiId
        
    def getDigits(self,str):
        c = ""
        for i in str:
            if i.isdigit():
                c+=i
        return c
        
    def updateTestCaseResult(self,_testCaseApiId,_status,_notes):
        conn = xmlrpc.Server(self.testLinkURL)
        data = {}
        data["devKey"] = self.devKey
        data["testcaseid"] = _testCaseApiId
        data["testplanid"] = self.testPlanId
        data["buildname"] = self.buildName
        data["status"] = _status
        data["notes"] = _notes
        updateTestResult = conn.tl.reportTCResult(data) 

#------------------------------------------------------------------------
#-- gets input from the user and pass it on to the _TestResult class
class TestLinkRunner():
    #-- Initializing variables
    def __init__(self,_testLinkURL,_devKey,_testPlanId, _buildName):
        self.testLinkURL = _testLinkURL
        self.devKey = _devKey
        self.testPlanId = _testPlanId
        self.buildName = _buildName
        
    #-- Calling the _TestResult with the necessary arguments
    def run(self,test):
        result = _TestResult(self.testLinkURL,self.devKey,self.testPlanId,self.buildName)
        test(result)
        
#-------------------------------------------------------------------------
#-- To redirect the output        
class OutputRedirector(object):
    """ Wrapper to redirect stdout or stderr """
    def __init__(self, fp):
        self.fp = fp
 
    def write(self, s):
        self.fp.write(s)
 
    def writelines(self, lines):
        self.fp.writelines(lines)
 
    def flush(self):
        self.fp.flush()
 
stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)
