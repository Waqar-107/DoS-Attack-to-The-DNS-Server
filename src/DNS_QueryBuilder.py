# from dust i have come, dust i will be

import socket
import binascii

class dns_query:
    def __init__(self):
        self.query_type = 0
        self.query_no = 1
        self.recursiveQuery = True
        self.truncated = False
        self.questionQuantity = 1
        self.domain_name = "-1"
        self.showReport = False
        self.showError = False

    # the binary representation will be returned, if the length is < desired digits then extra 0 is padded
    def __getBinary(self, number, digit):
        s = ""
        while number > 0:
            s += chr(number % 2 + ord('0'))
            number //= 2

        while len(s) < digit:
            s += '0'

        s = s[:: -1]
        return s

    # 0 : a standard query (QUERY), 1 : an inverse query (IQUERY), 2 : a server status request (STATUS)
    def setQueryType(self, query_type):
        self.query_type = query_type

    # set true or false - true by default
    def setRecusiveQuery(self, flag):
        self.recursiveQuery = flag

    # set true or false - false by default
    def setShowReport(self, flag):
        self.showReport = flag
    
    # set true or false - false by default
    def setShowError(self, flag):
        self.showError = flag
        
    # set domain name
    def setDomainName(self, name):
        self.domain_name = name
    
    def __buildHeader(self):
        header = ""

        # same will be returned in the response of the query - 16 bits
        ID = self.__getBinary(self.query_no, 16)

        # 1 4 1 1 1 1 3 4
        # |QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
        QR = "0"

        opcode = self.__getBinary(self.query_type, 4)

        AA = "0"
        TC = "1" if self.truncated else "0"
        RD = "1" if self.recursiveQuery else "0"
        RA = "0"

        Z = "000"
        RCODE = "0000"

        # number of questions
        QDCOUNT = self.__getBinary(self.questionQuantity, 16)

        ANCOUNT = self.__getBinary(0, 16)
        NSCOUNT = self.__getBinary(0, 16)
        ARCOUNT = self.__getBinary(0, 16)

        temp = ID + QR + opcode + AA + TC + RD + RA + Z + \
            RCODE + QDCOUNT + ANCOUNT + NSCOUNT + ARCOUNT

        # make the binary header hex
        for i in range(0, len(temp), 4):
            hx = hex(int(temp[i: i + 4], 2))
            header += hx[2:]

        return header

    def __buildQuestion(self):
        question_section = ""
        partitions = self.domain_name.split('.')

        QNAME = ""
        for p in partitions:
            QNAME += self.__getBinary(len(p), 8)

            for i in range(len(p)):
                QNAME += self.__getBinary(ord(p[i]), 8)

        # end of the domain
        QNAME += self.__getBinary(0, 8)

        # The DNS record type we’re looking up. We’ll be looking up A records, whose value is 1.
        QTYPE = self.__getBinary(1, 16)

        # The class we’re looking up. We’re using the the internet, IN, which has a value of 1
        QCLASS = self.__getBinary(1, 16)

        temp_question = QNAME + QTYPE + QCLASS

        # convert the question into hex
        # do not use extra padding!!!
        for i in range(0, len(temp_question), 4):
            hx = hex(int(temp_question[i: i + 4], 2))
            question_section += hx[2:]

        self.question_len = len(question_section)
        return question_section

    def __parseResponse(self, res):
        # ----------------------------------------
        # header
        head = []
        for i in range(0, 24, 4):
            head.append(res[i: i + 4])

        ID = head[0]
        flags = head[1]
        question_quantity = head[2]
        answer_quantity = head[3]
        authority_records = head[4]
        additional_records = head[5]

        # check id
        if(int(ID, 16) != self.query_no):
            if self.showError:
                print("error : id not matched")
                print("query-id :", self.query_no)
                print("response-id :", int(ID, 16))
            
            return "-1"

        self.query_no += 1

        # check flags
        flags = self.__getBinary(int(flags, 16), 16)

        # 1 4 1 1 1 1 3 4
        # |QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
        QR = flags[0]
        opcode = flags[1: 5]
        AA = flags[5]
        TC = flags[6]
        RD = flags[7]
        RA = flags[8]
        Z = flags[9: 12]
        RCODE = flags[12: 16]

        if int(RCODE, 2) != 0:
            if self.showError:
                print(RCODE, "error reported")
            
            return "-1"

        # additional info
        if self.showReport:
            print("No errors reported")

            if int(AA, 2) == 0:
                print("This server isn’t an authority for the given domain name")

            if int(RD, 2) == 1:
                print("Recursion was desired for this request")

            if int(RA, 2) == 1:
                print("Recursion is available on this DNS server")

        # ----------------------------------------

        # question section is the same as the query
        question = res[24: 24 + self.question_len]

        # ----------------------------------------
        # answer
        answer_section = res[24 + self.question_len:]

        # [12 : 16] => don't know the fuck it denotes, it is 00 00
        NAME = answer_section[0: 4]
        TYPE = answer_section[4: 8]
        CLASS = answer_section[8: 12]
        TTL = answer_section[16: 20]
        RDLENGTH = int(answer_section[20: 24], 16)
        RDDATA = answer_section[24:]

        if self.showReport:
            print("TTL :", int(TTL, 16), "seconds")
            print("RDLENGTH :", RDLENGTH, "bytes")

        ip_adress_chunks = []
        for i in range(0, RDLENGTH * 2, 2):
            ip_adress_chunks.append(str(int(RDDATA[i: i + 2], 16)))

        return ".".join(ip_adress_chunks)
        # ----------------------------------------

    def getDNSQuery(self):
        if self.domain_name == "-1":
            print("--- set domain name first !!! ---")
            return
        
        return self.__buildHeader() + self.__buildQuestion()
        
    def getIP(self, res):
        return self.__parseResponse(res)
