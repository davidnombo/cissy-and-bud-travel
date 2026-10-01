"""Scoped Launch Build 1 components, using the existing V3 page shell."""
import html
def odyssey_explainer(copy):
    esc = html.escape
    sections = {
        'GO SMALL. GO NOW.': 'Go Small. Go Now.',
        'WHY NOW?': 'Why now?',
        'THE PLAN, SUCH AS IT IS': 'The plan, such as it is',
        'WHAT ARE WE LOOKING FOR?': 'What are we looking for?',
        'AN INVITATION': 'An invitation',
    }
    body = '<header class="page-intro shell"><p class="kicker">The Transcontinental Odyssey / The whole idea</p><h1>What the Hell Is the Odyssey?</h1><p class="kicker">The plan, with room to change</p><p class="intro">About 52 Weeks · Roughly 50,000 Miles · Key West to Deadhorse</p></header>'
    body += '<article class="shell odyssey-explainer"><div class="prose">'
    for paragraph in copy[1:]:
        if paragraph in sections:
            body += f'<h2>{sections[paragraph]}</h2>'
        elif paragraph.startswith('PRIUS V →'):
            body += '<div class="vehicle-progression" aria-label="From our first road trips to our Alaska ambition"><ol>' + ''.join(f'<li>{esc(vehicle)}</li>' for vehicle in ['Prius V', 'Town & Country', 'Sprinter 4x4', 'Alaska']) + '</ol><p>Go Small. Go Now.</p></div>'
        elif paragraph == 'It started with Alaska.':
            body += f'<p class="lead">{esc(paragraph)}</p>'
        else:
            body += f'<p>{esc(paragraph)}</p>'
        if paragraph == 'The Transcontinental Odyssey.':
            body += '<aside class="odyssey-route" aria-label="Broad planned route"><p class="kicker">Positioning the Van for Launch</p><h2>A continent, three chapters.</h2><p>A broad plan, with Alaska at its heart and Deadhorse an ambition.</p><ol><li><h3>The slingshot</h3><p>Cincinnati / Warsaw area → Northern California / Jenner and the wedding → Southern California and the Southwest → Key West → Cincinnati</p></li><li><h3>The launch</h3><p>Cincinnati → Calgary, Banff and Jasper → Alaska, with an Arctic ambition</p></li><li><h3>The long way home</h3><p>Alaska → Canada → Vancouver and the Pacific Northwest → Jenner</p></li></ol></aside>'
    body += '<nav class="story-next" aria-label="Follow the Odyssey"><p class="kicker">Come along for the ride</p><a class="text-link" href="./#dispatches">Follow the Odyssey <span aria-hidden="true">↗</span></a></nav></div></article>'
    return body
