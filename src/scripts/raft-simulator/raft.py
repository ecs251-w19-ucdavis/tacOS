from enum import Enum
from threading import Thread
import time

# Defined by me.
from state_machine import StateMachine
from log import Log

# TODO: remove this class
class Temp:
    NUM_SERVERS = 5
    HEARTBEAT_PERIOD = 1  # in seconds
    servers = []

# Represents a request from a client.
class Request:
    def __init__(self, command):
        self.command = command  # says how to change the state machine

# Public API:
#   __init__(): (constructor) 
#   handle_request()
#   append_entries_RPC()
#   request_vote_RPC()
class RaftServer:

    # Miscellaneous constants.
    NO_LEADER = -1

    def __init__(self, id):
        self.id = id  # unique id for this RaftServer
        
        self.state_machine = StateMachine()

        # Persistent state on a server.
        self.current_term = 0
        self.voted_for = None  # candidate_id that received vote
                               # in current term
        self.log = Log()

        # Volatile state on a server.
        self.commit_index = 0   # index of highest log entry known
                                # to be committed
        self.last_applied = 0   # index of highest log entry applied
                                # to state machine

        # Volatile state on a leader. (Reinitialized after election.)
        # for each server, index of next log
        # entry to send to that server:
        self.next_index = []
        # for each server, index of highest
        # log entry known to be replicated on server:
        self.match_index = []

        self.leader_id = self.NO_LEADER
        
        self.num_votes = 0  # votes for this candidate
        self.state = self.State.FOLLOWER
        self.heartbeat_thread = None  # for leader to assert authority
        self.candidate_thread = None  # for candidate to grab votes
        self.election_timeout = 100  # random number for now

    def __del__(self):
        if self.heartbeat_thread != None:
            self.state = self.State.FOLLOWER  # kills thread
            self.heartbeat_thread.join()  # wait for thread to die

    class State(Enum):
        FOLLOWER = 1
        CANDIDATE = 2
        LEADER = 3

    def __got_majority_vote(self):
        return self.num_votes > Temp.NUM_SERVERS / 2

    def __request_votes(self):
        # Send out vote requests.
        # TODO: reset election timer
        # TODO: select new randomized election timeout
        # send Requestvote RPCs to all other servers:
        # for i in range(Temp.NUM_SERVERS):
        #     if i != self.id:
        #         response = Temp.servers[i].request_vote_RPC(
        #             self.current_term, self.id, self.log.size()-1,
        #             self.log.latest())
        #         print("Thread {}: thread {} sent {} back to me".format(
        #             self.id, i, response))

        # Keep spinning UNTIL either:
        # a) election timeout 
        # b) got majority vote
        while (not self.__got_majority_vote() and
            self.leader_id == self.NO_LEADER):
            pass
        print("Thread {} broke out candidate loop".format(self.id))

        if self.__got_majority_vote():  # this server was elected
            self.__become_leader()
        elif self.leader_id != self.NO_LEADER:  # other server was elected
            self.__become_follower()
        else:  # timed out
            self.__start_election()

    def __become_candidate(self):
        print("Thread {} has become candidate".format(self.id))
        # Start candidate thread.
        self.candidate_thread = Thread(target=self.__start_election)
        self.candidate_thread.start()

    # Called if no communication from leader and
    # election timeout reached.
    def __start_election(self):
        self.current_term += 1
        self.num_votes = 0
        assert(self.state != self.State.LEADER)  # can't start election if was Leader
        self.state = self.State.CANDIDATE
        self.voted_for = self.id
        self.leader_id = self.NO_LEADER
        self.__request_votes()

    # For heartbeat thread.
    # If leader, sends heartbeat to all followers,
    # then wait until must send next heartbeat.
    def __send_heartbeat(self):
        while self.state == self.State.LEADER:
            # for each follower
                # send empty AppendEntries RPC
            for i in range(Temp.NUM_SERVERS):
                if i != self.id:
                    prev_log_index = self.next_index[i] - 1
                    response = Temp.servers[i].append_entries_RPC(self.current_term,
                        self.id,
                        #  these next two params might be wrong
                        prev_log_index, self.log.get(prev_log_index).term,
                        [],  # because heartbeat
                        self.commit_index)
                    # print("Thread {}: thread {} sent {} back to me".format(
                        # self.id, i, response))
            # print("Thread id={} sending heartbeat".format(self.id))
            time.sleep(Temp.HEARTBEAT_PERIOD)

    def __become_leader(self):
        print("Thread {} has become leader".format(self.id))
        self.state = self.State.LEADER
        initial_next_index = self.last_applied + 1
        self.next_index = [initial_next_index] * Temp.NUM_SERVERS
        self.match_index = [0] * Temp.NUM_SERVERS

        # Start heartbeat thread.
        self.heartbeat_thread = Thread(target=self.__send_heartbeat)
        self.heartbeat_thread.start()

    def __become_follower(self):
        print("Thread {} has become follower".format(self.id))
        self.state = self.State.FOLLOWER
        if self.heartbeat_thread != None:  # kill heartbeat thread (if any)
            self.heartbeat_thread.join()
            self.heartbeat_thread = None
        # TODO: what else?

    def __handle_request(self, request):
        self.log.append(self.current_term, request.command)

    # Used to receive request from client.
    # @request must be instance of Request.
    def handle_request(self, request):
        if self.state == RaftServerState.LEADER:
            # print("Thread {} handling request".format(self.id))
            self.__handle_request(request)
        else:
            assert(self.leader_id != self.NO_LEADER)
            Temp.servers[self.leader_id].handle_request(request)

    # Invoked by the leader on other raft servers to replicate
    # log entries. Also used as a heartbeat.
    # Simulates an RPC.
    # Output: tuple (@term, @success), where @term is the
    # current term, and @success indicating success (boolean).
    def append_entries_RPC(self, term, leader_id, prev_log_index,
                           prev_log_term, entries,
                           leader_commit):
        # print("Thread {} handling AppendEntries RPC".format(self.id))

        if self.id == leader_id:  # if leader sent RPC to itself
            raise AssertionError("Leader sent AppendEntries RPC to itself")

        if term < self.current_term:
            return (self.current_term, False)
        if (self.log.len() <= prev_log_index
            or self.log.get(prev_log_index).term != prev_log_term):
            return (self.current_term, False)
        # TODO: #3 and 4 and 5
        # if leader_commit > self.commit_index:
            # self.commit_index = min(leader_commit, (index of last new entry))
        
        if self.leader_id == self.NO_LEADER:  # if hasn't acknowledged this leader
            self.leader_id = leader_id
            # if self.state != self.State.FOLLOWER:
            #     self.__become_follower()
        return (self.current_term, True)

    # Invoked by candidates on other raft servers to gather votes.
    def request_vote_RPC(term, candidate_id, last_log_index,
                         last_log_term):
        if term < self.current_term:  # requester's log is out of date
            return (self.current_term, False)
        if self.voted_for == None or self.voted_for == candidate_id:
            return (self.current_term, True)
        else:  # already voted for somene else
            return (self.current_term, False)

    # TODO: remove
    def make_leader(self):
        self.__become_leader()
    def make_follower(self):
        self.__become_follower()
    def make_candidate(self):
        self.__become_candidate()
    def leader_die(self):
        self.__become_follower()  # stop sending heartbeats
    def add_vote(self):
        self.num_votes += 1

class RaftServerTest:
    def __init__(self):
        for i in range(Temp.NUM_SERVERS):
            Temp.servers.append(RaftServer(i))
        # Temp.servers[2].make_leader()

    def print_states(self):
        for i in range(Temp.NUM_SERVERS):
            print("====== Thread {} ======".format(i))
            print("State: ", Temp.servers[i].state)
            print("Current term: ", Temp.servers[i].current_term)
