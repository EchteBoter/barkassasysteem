import sys
import telepot
import time
from telepot.loop import MessageLoop
from telepot.delegate import pave_event_space, per_inline_from_id, create_open
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent

class QueryCounter(telepot.helper.InlineUserHandler, telepot.helper.AnswererMixin):
    def __init__(self, *args, **kwargs):
        super(QueryCounter, self).__init__(*args, **kwargs)
        self._count = 0

    def on_inline_query(self, msg):
        def compute():
            query_id, from_id, query_string = telepot.glance(msg, flavor="inline_query")
            print(self.id, ':', 'InlineQuery:', query_id, from_id, query_string)

            self._count += 1
            text = '%d. %s' % (self._count, query_string)

            articles = [InlineQueryResultArticle(
                id='abc',
                title=text,
                input_message_content=InputTextMessageContetn(
                    message_text=text
                )
            )]

            return articles

        self.answerer.answer(msg, compute)
    
    def on_chosen_inline_result(self, msg):
        result_id, from_id, query_string  = telepot.glance(msg, flavor='chosen_inline_result')
        print(self.id, ':', 'Chosen Inline Result:', result_id, from_id, query_string)

TOKEN = sys.argv[1]
#TOKEN = '466467969:AAHZ253Zam0jPyJaqTxQZ6baCbWnvatsxt4'

bot = telepot.DelegatorBot(TOKEN, [
pave_event_space()(
    per_inline_from_id(), create_open, QueryCounter, timeout=10),
])

#def handle(msg):
#    print(msg)


#MessageLoop(bot, handle).run_as_thread()
#print ('Listening ...')
while 1:
    time.sleep(10)