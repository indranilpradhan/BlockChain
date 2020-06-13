from random import randint
from random import seed
from random import randint
import hashlib
import Crypto.Util.number
import sys
from Crypto import Random
import random

class Node:  
    def __init__(self, data): 
        self.data = data
        self.next = None

class HashPtNode:
    def __init__(self,data):
        self.data = data
        self.hashNext = None
        self.next = None

class HashSignPtNode:
    def __init__(self,data):
        self.data = data
        self.hashNext = 2
        self.signNext = 2
        self.next = None

class LinkedList:  
    def __init__(self): 
        self.head = None
        self.last = None

    def push(self, head, last, data):
        temp = Node(data)
        if(head == None and last == None):
            head = temp
            last = head
        else:
            last.next = temp
            last = temp
        return head,last

    def pop(self,head,last):
        if(head == None):
            return None
        else:
            if(head == last):
                head = None
                last = None
                return None
            temp = head
            while(temp.next != last):
                temp = temp.next
            last = temp
            last.next = None
            return head,last

    def traverselist(self, head): 
        temp = head 
        while (temp): 
            print(temp.data,)#hex(id(temp.next))) 
            temp = temp.next

class HashPtLinkedList:
    def __init__(self): 
        self.head = None
        self.last = None
        self.q = self.choosing_p(5)
        self.g = self.generator(self.q)
        self.z = self.calculate_z(self.g, self.q)
        self.x = self.generating_x(self.g)
        self.k = 13
        self.check_node = HashPtNode(0)

    def convert_string_asciisum(self,m):
        asc = [ord(c) for c in m]
        return sum(asc)

    def calculate_z(self,g,q):
        temp = randint(1,q-1)
        z = (g**temp)%q
        return z

    def hash_function(self,x1,x2):
        hash_val = ((self.g**x1)%self.q * (self.z**x2)%self.q)%self.q
        return hash_val

    def loop_exponent(self,exponent, nr, r, p):
        while(nr != 1):
            nr = (nr*r)%p
            exponent= exponent+1
        return exponent

    def generating_x(self,g):
        x = randint(1,g-1)
        return x

    def loop_gen(self,nr, exponent, r, p, g):
        exponent = self.loop_exponent(exponent, nr, r, p)
        if(exponent == p-1 and exponent != None):
            g.append(r)

    def generator(self,p):
        g = []
        for i in range(1,p):
            r = i
            exponent = 1
            nr = r%p
            self.loop_gen(nr, exponent, r, p, g)
        return random.choice(g)

    def choosing_p(self,n):
        q = Crypto.Util.number.getPrime(n, randfunc=Random.get_random_bytes)
        return q

    def hash_(self,m):
        M = self.convert_string_asciisum(m)
        r = (self.g**self.k)%self.q
        h = (self.hash_function(r,M))
        return h
    
    def push(self, head, last, data):
        temp = HashPtNode(data)
        if(head == None and last == None):
            temp.next = self.check_node
            temphashNext = str(temp.hashNext)
            tempAddr = str(hex(id(temp.next)))
            message = temphashNext+tempAddr+str(temp.data)
            hash_message = self.hash_(message)
            self.check_node.hashNext = hash_message
            head = temp
            last = head
        else:
            temp.next = self.check_node
            last.next = temp
            lasthashNext= str(last.hashNext)
            lastAddr = str(hex(id(last.next)))
            lastmessage = lasthashNext+lastAddr+str(last.data)
            last_hash_message = self.hash_(lastmessage)
            temp.hashNext = last_hash_message
            last = temp
            lasthashNext = str(last.hashNext)
            lastAddr = str(hex(id(last.next)))
            lastmessage = lasthashNext+lastAddr+str(last.data)
            last_hash_message = self.hash_(lastmessage)
            self.check_node.hashNext = last_hash_message

        return head,last

    def pop(self,head,last):
        if(head == None):
            return None
        else:
            if(head == last):
                head = None
                last = None
                return None
            temp = head
            while(temp.next != last):
                temp = temp.next
            #check_node = temp.next.next
            last = temp
            last.next = self.check_node
            lasthashNext = str(last.hashNext)
            lastAddr = str(hex(id(last.next)))
            lastmessage = lasthashNext+lastAddr+str(last.data)
            last_hash_message = self.hash_(lastmessage)
            self.check_node.hashNext = last_hash_message

            return head,last

    def traverselist(self, head, last): 
        temp = head 
        while (temp != last.next): 
            print(temp.data) 
            temp = temp.next

    def verify(self, head, last):
        nodes = -1
        temp = head 
        i =0
        while (temp != last.next):
            thashNext = str(temp.hashNext)
            tAddr = str(hex(id(temp.next)))
            tmessage = thashNext+tAddr+str(temp.data)
            t_hash_message = self.hash_(tmessage) 
            if(t_hash_message != temp.next.hashNext):
                nodes = i
                return nodes
            i = i+1
            temp = temp.next
        return nodes

class HashSignPtLinkedList:
    def __init__(self): 
        self.head = None
        self.last = None
        self.q = self.choosing_p(5)
        self.g = self.generator(self.q)
        self.z = self.calculate_z(self.g, self.q)
        self.y,self.x = self.generating_x(self.g)
        self.k = 13
        self.check_node = HashSignPtNode(0)

    def convert_string_asciisum(self,m):
        asc = [ord(c) for c in m]
        return sum(asc)

    def calculate_z(self,g,q):
        temp = randint(1,q-1)
        z = (g**temp)%q
        return z

    def hash_function(self,x1,x2):
        hash_val = ((self.g**x1)%self.q * (self.z**x2)%self.q)%self.q
        return hash_val

    def loop_exponent(self,exponent, nr, r, p):
        while(nr != 1):
            nr = (nr*r)%p
            exponent= exponent+1
        return exponent

    def generating_x(self,g):
        x = randint(1,g-1)
        y = (self.g**x)%self.q
        return y,x

    def loop_gen(self,nr, exponent, r, p, g):
        exponent = self.loop_exponent(exponent, nr, r, p)
        if(exponent == p-1 and exponent != None):
            g.append(r)

    def generator(self,p):
        g = []
        for i in range(1,p):
            r = i
            exponent = 1
            nr = r%p
            self.loop_gen(nr, exponent, r, p, g)
        return random.choice(g)

    def choosing_p(self,n):
        q = Crypto.Util.number.getPrime(n, randfunc=Random.get_random_bytes)
        return q

    def digital_signature(self,m):
        M = self.convert_string_asciisum(m)
        r = (self.g**self.k)%self.q
        h = (self.hash_function(r,M))
        s = (self.k-(self.x*h))%(self.q-1)
        return s,h

    def verifier(self,m,s,e):
        M = self.convert_string_asciisum(m)
        h_s = (self.g**s)%self.q
        h_y = (self.y**e)%self.q
        rv = (h_s*h_y)%self.q
        ev = (self.hash_function(rv,M))
        return ev

    def hash_(self,m):
        M = self.convert_string_asciisum(m)
        r = (self.g**self.k)%self.q
        h = (self.hash_function(r,M))
        return h
    
    def push(self, head, last, data):
        temp = HashSignPtNode(data)
        if(head == None and last == None):
            temp.next = self.check_node
            temphashNext = str(temp.hashNext)
            tempsignNext = str(temp.signNext)
            tempAddr = str(hex(id(temp.next)))
            message = temphashNext+tempsignNext+tempAddr+str(temp.data)
            hash_sign,hash_message = self.digital_signature(message)
            self.check_node.hashNext = hash_message
            self.check_node.signNext = hash_sign
            head = temp
            last = head
        else:
            temp.next = self.check_node
            last.next = temp
            lasthashNext= str(last.hashNext)
            lastsignNext = str(last.signNext)
            lastAddr = str(hex(id(last.next)))
            lastmessage = lasthashNext+lastsignNext+lastAddr+str(last.data)
            #print(lasthashNext,lastsignNext)
            last_hash_sign,last_hash_message = self.digital_signature(lastmessage)
            #print(last_hash_message,last_hash_sign)
            temp.hashNext = last_hash_message
            temp.signNext = last_hash_sign
            last = temp
            lasthashNext = str(last.hashNext)
            lastsignNext = str(last.signNext)
            lastsignNext = str(last.signNext)
            lastAddr = str(hex(id(last.next)))
            lastmessage = lasthashNext+lastsignNext+lastAddr+str(last.data)
            last_hash_sign,last_hash_message = self.digital_signature(lastmessage)
            self.check_node.hashNext = last_hash_message
            self.check_node.signNext = last_hash_sign
        return head,last

    def pop(self,head,last):
        if(head == None):
            return None
        else:
            if(head == last):
                head = None
                last = None
                return None
            temp = head
            while(temp.next != last):
                temp = temp.next

            last = temp
            last.next = self.check_node
            lasthashNext = str(last.hashNext)
            lastsignNext = str(last.signNext)
            lastAddr = str(hex(id(last.next)))
            lastmessage = lasthashNext+lastsignNext+lastAddr+str(last.data)
            last_hash_sign,last_hash_message = self.digital_signature(lastmessage)
            self.check_node.hashNext = last_hash_message
            self.check_node.signNext = last_hash_sign
            return head,last

    def traverselist(self, head, last): 
        temp = head 
        while (temp != last.next): 
            print(temp.data) 
            temp = temp.next

    def verify(self, head, last):
        nodes = -1
        temp = head 
        i =0
        while (temp != last.next):
            thashNext = str(temp.next.hashNext)
            thash = str(temp.hashNext)
            tsignNext = str(temp.next.signNext)
            tsign = str(temp.signNext)
            tAddr = str(hex(id(temp.next)))
            tmessage = thash+tsign+tAddr+str(temp.data)      
            t_hash_message = self.verifier(tmessage,int(tsignNext),int(thashNext))
            if(t_hash_message != temp.next.hashNext):
                nodes = i
                return nodes
            i = i+1
            temp = temp.next
        return nodes

if __name__=='__main__':
    print("++++++Pointer++++++++") 
    ll = LinkedList() 
    ll.head,ll.last = ll.push(ll.head,ll.last,1)
    ll.head,ll.last = ll.push(ll.head,ll.last,2)
    ll.head,ll.last = ll.push(ll.head,ll.last,3)
    ll.traverselist(ll.head)

    print("+++++++Hash pointer++++++++")
    llhspt = HashPtLinkedList()
    llhspt.head,llhspt.last = llhspt.push(llhspt.head,llhspt.last,1)
    llhspt.head,llhspt.last = llhspt.push(llhspt.head,llhspt.last,2)
    llhspt.head,llhspt.last = llhspt.push(llhspt.head,llhspt.last,3)
    llhspt.traverselist(llhspt.head,llhspt.last)
    node = llhspt.verify(llhspt.head,llhspt.last)
    if(node == -1):
        print("Verified")
    else:
        print("The modfied node ",node)
    print("=======modifying node======")
    llhspt.head.next.data = 5
    node = llhspt.verify(llhspt.head,llhspt.last)
    if(node == -1):
        print("Verified")
    else:
        print("The modfied node ",node)


    print("++++++Hash sign pointer++++++++")
    llhsSgnpt = HashSignPtLinkedList()
    llhsSgnpt.head,llhsSgnpt.last = llhsSgnpt.push(llhsSgnpt.head,llhsSgnpt.last,1)
    llhsSgnpt.head,llhsSgnpt.last = llhsSgnpt.push(llhsSgnpt.head,llhsSgnpt.last,2)
    llhsSgnpt.head,llhsSgnpt.last = llhsSgnpt.push(llhsSgnpt.head,llhsSgnpt.last,3)
    llhsSgnpt.traverselist(llhsSgnpt.head,llhsSgnpt.last)
    node = llhsSgnpt.verify(llhsSgnpt.head,llhsSgnpt.last)
    if(node == -1):
        print("Verified")
    else:
        print("The modfied node ",node)
    print("======modifying node=======")
    llhsSgnpt.head.next.next.data = 5
    node = llhsSgnpt.verify(llhsSgnpt.head,llhsSgnpt.last)
    if(node == -1):
        print("Verified")
    else:
        print("The modfied node ",node)

  
  