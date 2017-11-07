# encoding: utf8

from quantiphy import Quantity
import sys

class Case:
    def __init__(self, name, text, raw, formatted, prefs=None):
        self.name = name
        self.text = text
        self.raw = raw
        self.formatted = formatted
        self.prefs = prefs

py3 = int(sys.version[0]) == 3

test_cases = [
    Case('grange', '0', ('0', ''), '0'),
    Case('waltz', '0s', ('0', 's'), '0s'),
    Case('allay', '0 s', ('0', 's'), '0s'),
    Case('tribute', '$0', ('0', '$'), '$0'),
    Case('lunatic', '1', ('1', ''), '1'),
    Case('seafront', '1s', ('1', 's'), '1s'),
    Case('birthday', '1 s', ('1', 's'), '1s'),
    Case('energy', '$1', ('1', '$'), '$1'),
    Case('loser', '2.', ('2', ''), '2'),
    Case('disprove', '2.s', ('2', 's'), '2s'),
    Case('mixture', '2. s', ('2', 's'), '2s'),

    # test all the scale factors
    Case('quill', '1ys', ('1e-24', 's'), '1e-24s'),
    Case('joust', '1zs', ('1e-21', 's'), '1e-21s'),
    Case('streak', '1as', ('1e-18', 's'), '1as'),
    Case('mutiny', '1fs', ('1e-15', 's'), '1fs'),
    Case('banker', '1ps', ('1e-12', 's'), '1ps'),
    Case('conquer', '1ns', ('1e-9', 's'), '1ns'),
    Case('share', '1us', ('1e-6', 's'), '1us'),
    Case('resurface', '1μs', ('1e-6', 's'), '1us') if py3 else None,
        # fails on python2, so skip it.
    Case('witch', '1ms', ('1e-3', 's'), '1ms'),
    Case('engrave', '1cs', ('10e-3', 's'), '10ms'),
    Case('finance', '1_s', ('1', 's'), '1s'),
    Case('ecologist', '1ks', ('1e3', 's'), '1ks'),
    Case('insulate', '1Ks', ('1e3', 's'), '1ks'),
    Case('apprehend', '1Ms', ('1e6', 's'), '1Ms'),
    Case('hoarding', '1Gs', ('1e9', 's'), '1Gs'),
    Case('scrum', '1Ts', ('1e12', 's'), '1Ts'),
    Case('tissue', '1Ps', ('1e15', 's'), '1e15s'),
    Case('panorama', '1Es', ('1e18', 's'), '1e18s'),
    Case('quest', '1Zs', ('1e21', 's'), '1e21s'),
    Case('suture', '1Ys', ('1e24', 's'), '1e24s'),

    # test zero
    Case('nickel', '0ns', ('0', 's'), '0s'),
    Case('sprinkle', '0 ns', ('0', 's'), '0s'),
    Case('seclude', '00ns', ('0', 's'), '0s'),
    Case('semester', '000ns', ('0', 's'), '0s'),
    Case('jackboot', '0.ns', ('0', 's'), '0s'),
    Case('universal', '0. ns', ('0', 's'), '0s'),
    Case('abduct', '00.ns', ('0', 's'), '0s'),
    Case('forehead', '000.ns', ('0', 's'), '0s'),
    Case('expire', '.0ns', ('0', 's'), '0s'),
    Case('rigidity', '.0 ns', ('0', 's'), '0s'),
    Case('inspector', '.00ns', ('0', 's'), '0s'),
    Case('gumdrop', '.000ns', ('0', 's'), '0s'),
    Case('prairie', '0ns', ('0', 's'), '0s', {'prec':'full'}),
    Case('misapply', '0 ns', ('0', 's'), '0s', {'prec':'full'}),
    Case('avenue', '00ns', ('0', 's'), '0s', {'prec':'full'}),
    Case('socket', '000ns', ('0', 's'), '0s', {'prec':'full'}),
    Case('revise', '.0ns', ('0', 's'), '0s', {'prec':'full'}),
    Case('jerkin', '.0 ns', ('0', 's'), '0s', {'prec':'full'}),
    Case('blackhead', '.00ns', ('0', 's'), '0s', {'prec':'full'}),
    Case('fathead', '.000ns', ('0', 's'), '0s', {'prec':'full'}),

    # test various forms of the mantissa when using scale factors
    Case('delicacy', '1ns', ('1e-9', 's'), '1ns'),
    Case('huntsman', '1 ns', ('1e-9', 's'), '1ns'),
    Case('weighty', '10ns', ('10e-9', 's'), '10ns'),
    Case('madrigal', '100ns', ('100e-9', 's'), '100ns'),
    Case('comport', '.1ns', ('100e-12', 's'), '100ps'),
    Case('character', '.1 ns', ('100e-12', 's'), '100ps'),
    Case('sharpen', '.10ns', ('100e-12', 's'), '100ps'),
    Case('resonate', '.100ns', ('100e-12', 's'), '100ps'),
    Case('replica', '1.ns', ('1e-9', 's'), '1ns'),
    Case('parachute', '1. ns', ('1e-9', 's'), '1ns'),
    Case('merger', '10.ns', ('10e-9', 's'), '10ns'),
    Case('grating', '100.ns', ('100e-9', 's'), '100ns'),
    Case('enjoyment', '1.0ns', ('1e-9', 's'), '1ns'),
    Case('refit', '1.0 ns', ('1e-9', 's'), '1ns'),
    Case('thread', '10.0ns', ('10e-9', 's'), '10ns'),
    Case('upright', '100.0ns', ('100e-9', 's'), '100ns'),
    Case('inscribe', '1.00ns', ('1e-9', 's'), '1ns'),
    Case('warrior', '1.00 ns', ('1e-9', 's'), '1ns'),
    Case('paranoiac', '10.00ns', ('10e-9', 's'), '10ns'),
    Case('genie', '100.00ns', ('100e-9', 's'), '100ns'),
    Case('persimmon', '-1.00ns', ('-1e-9', 's'), '-1ns'),
    Case('barnacle', '-1.00 ns', ('-1e-9', 's'), '-1ns'),
    Case('dialog', '-10.00ns', ('-10e-9', 's'), '-10ns'),
    Case('bright', '-100.00ns', ('-100e-9', 's'), '-100ns'),
    Case('mutate', '+1.00ns', ('1e-9', 's'), '1ns'),
    Case('session', '+1.00 ns', ('1e-9', 's'), '1ns'),
    Case('capillary', '+10.00ns', ('10e-9', 's'), '10ns'),
    Case('twinkle', '+100.00ns', ('100e-9', 's'), '100ns'),

    # test various forms of the mantissa when using exponents
    Case('hairpiece', '1e-9s', ('1e-9', 's'), '1ns'),
    Case('marble', '10E-9s', ('10e-9', 's'), '10ns'),
    Case('boomerang', '100e-9s', ('100e-9', 's'), '100ns'),
    Case('antiquity', '.1e-9s', ('100e-12', 's'), '100ps'),
    Case('redhead', '.10E-9s', ('100e-12', 's'), '100ps'),
    Case('rarity', '.100e-9s', ('100e-12', 's'), '100ps'),
    Case('latecomer', '1.e-9s', ('1e-9', 's'), '1ns'),
    Case('blackball', '10.E-9s', ('10e-9', 's'), '10ns'),
    Case('sweetener', '100.e-9s', ('100e-9', 's'), '100ns'),
    Case('kidney', '1.0E-9s', ('1e-9', 's'), '1ns'),
    Case('erode', '10.0e-9s', ('10e-9', 's'), '10ns'),
    Case('omelet', '100.0E-9s', ('100e-9', 's'), '100ns'),
    Case('mealy', '1.00e-9s', ('1e-9', 's'), '1ns'),
    Case('chaser', '10.00E-9s', ('10e-9', 's'), '10ns'),
    Case('skitter', '100.00e-9s', ('100e-9', 's'), '100ns'),
    Case('romantic', '-1.00E-9s', ('-1e-9', 's'), '-1ns'),
    Case('bohemian', '-10.00e-9s', ('-10e-9', 's'), '-10ns'),
    Case('forbid', '-100.00E-9s', ('-100e-9', 's'), '-100ns'),
    Case('quartet', '+1.00e-9s', ('1e-9', 's'), '1ns'),
    Case('presume', '+10.00E-9s', ('10e-9', 's'), '10ns'),
    Case('trouper', '+100.00e-9s', ('100e-9', 's'), '100ns'),
    Case('particle', '+.1E-9s', ('100e-12', 's'), '100ps'),
    Case('defeat', '+.10e-9s', ('100e-12', 's'), '100ps'),
    Case('oxcart', '+.100E-9s', ('100e-12', 's'), '100ps'),
    Case('creaky', '-.1e-9s', ('-100e-12', 's'), '-100ps'),
    Case('gentleman', '-.10E-9s', ('-100e-12', 's'), '-100ps'),
    Case('spangle', '-.100e-9s', ('-100e-12', 's'), '-100ps'),

    # test various forms of the mantissa alone
    Case('educate', '100000.0s', ('100e3', 's'), '100ks'),
    Case('headline', '100000 s', ('100e3', 's'), '100ks'),
    Case('protein', '10000s', ('10e3', 's'), '10ks'),
    Case('increase', '10000.0 s', ('10e3', 's'), '10ks'),
    Case('response', '1000.0s', ('1e3', 's'), '1ks'),
    Case('parodist', '1000 s', ('1e3', 's'), '1ks'),
    Case('speck', '100s', ('100', 's'), '100s'),
    Case('chihuahua', '100.0 s', ('100', 's'), '100s'),
    Case('couch', '10.0s', ('10', 's'), '10s'),
    Case('highbrow', '10 s', ('10', 's'), '10s'),
    Case('haughty', '1s', ('1', 's'), '1s'),
    Case('break', '1.0 s', ('1', 's'), '1s'),
    Case('gutter', '0.1s', ('100e-3', 's'), '100ms'),
    Case('ability', '0.1 s', ('100e-3', 's'), '100ms'),
    Case('atone', '0.01s', ('10e-3', 's'), '10ms'),
    Case('essential', '0.01 s', ('10e-3', 's'), '10ms'),
    Case('godmother', '0.001s', ('1e-3', 's'), '1ms'),
    Case('temper', '0.001 s', ('1e-3', 's'), '1ms'),
    Case('verse', '0.0001s', ('100e-6', 's'), '100us'),
    Case('fifth', '0.0001 s', ('100e-6', 's'), '100us'),
    Case('horsewhip', '0.00001s', ('10e-6', 's'), '10us'),
    Case('larch', '0.00001 s', ('10e-6', 's'), '10us'),

    # test various forms of units
    Case('impute', '1ns', ('1e-9', 's'), '1ns'),
    Case('eyesore', '1e-9s', ('1e-9', 's'), '1ns'),
    Case('aspirant', '1n', ('1e-9', ''), '1n'),
    Case('delete', '1e-9', ('1e-9', ''), '1n'),
    Case('flummox', '1 ns', ('1e-9', 's'), '1ns'),
    Case('foster', '1 e-9 s', None, '1ns'),
    Case('deforest', '1n s', None, '1ns'),
    Case('fortune', '1e-9 s', ('1e-9', 's'), '1ns'),
    Case('starchy', '1nm/s', ('1e-9', 'm/s'), '1nm/s'),
    Case('preamble', '1e-9m/s', ('1e-9', 'm/s'), '1nm/s'),
    Case('haversack', '1 nm/s', ('1e-9', 'm/s'), '1nm/s'),
    Case('sprinter', '1e-9 m/s', ('1e-9', 'm/s'), '1nm/s'),
    Case('descend', '1nJ-s', ('1e-9', 'J-s'), '1nJ-s'),
    Case('milieu', '1e-9J-s', ('1e-9', 'J-s'), '1nJ-s'),
    Case('force', '1 nJ-s', ('1e-9', 'J-s'), '1nJ-s'),
    Case('athletic', '1e-9 J-s', ('1e-9', 'J-s'), '1nJ-s'),
    Case('scaffold', '1nm(s^-1)', ('1e-9', 'm(s^-1)'), '1nm(s^-1)'),
    Case('incur', '1e-9m(s^-1)', ('1e-9', 'm(s^-1)'), '1nm(s^-1)'),
    Case('hornet', '1 nm(s^-1)', ('1e-9', 'm(s^-1)'), '1nm(s^-1)'),
    Case('fledgling', '1e-9 m(s^-1)', ('1e-9', 'm(s^-1)'), '1nm(s^-1)'),
    Case('amnesty', '1nm/s^2', ('1e-9', 'm/s^2'), '1nm/s^2'),
    Case('carpet', '1e-9m/s^2', ('1e-9', 'm/s^2'), '1nm/s^2'),
    Case('intrigue', '1 nm/s^2', ('1e-9', 'm/s^2'), '1nm/s^2'),
    Case('picky', '1e-9 m/s^2', ('1e-9', 'm/s^2'), '1nm/s^2'),

    # test currency
    Case('bishop', '$10K', ('10e3', '$'), '$10k'),
    Case('colonnade', '$10', ('10', '$'), '$10'),
    Case('wizard', '$10.00', ('10', '$'), '$10'),
    Case('stork', '$10e9', ('10e9', '$'), '$10G'),
    Case('walkover', '$0.01', ('10e-3', '$'), '$10m'),
    Case('kinswoman', '$.01', ('10e-3', '$'), '$10m'),
    Case('valuable', '$1.', ('1', '$'), '$1'),
    Case('kiddie', '-$10K', ('-10e3', '$'), '-$10k'),
    Case('breather', '-$10', ('-10', '$'), '-$10'),
    Case('recoil', '-$10.00', ('-10', '$'), '-$10'),
    Case('wrestle', '-$10e9', ('-10e9', '$'), '-$10G'),
    Case('theorist', '-$0.01', ('-10e-3', '$'), '-$10m'),
    Case('neurone', '-$.01', ('-10e-3', '$'), '-$10m'),
    Case('crevice', '-$1.', ('-1', '$'), '-$1'),
    Case('bodice', '+$10K', ('10e3', '$'), '$10k'),
    Case('homicide', '+$10', ('10', '$'), '$10'),
    Case('plural', '+$10.00', ('10', '$'), '$10'),
    Case('guidebook', '+$10e9', ('10e9', '$'), '$10G'),
    Case('weaken', '+$0.01', ('10e-3', '$'), '$10m'),
    Case('subtlety', '+$.01', ('10e-3', '$'), '$10m'),
    Case('flywheel', '+$1.', ('1', '$'), '$1'),

    # test unusual numbers
    Case('sheathe', 'inf', ('inf', ''), 'inf'),
    Case('integrate', 'inf Hz', ('inf', 'Hz'), 'inf Hz'),
    Case('witter', '$inf', ('inf', '$'), '$inf'),
    Case('smoker', '-inf', ('-inf', ''), '-inf'),
    Case('spittoon', '-inf Hz', ('-inf', 'Hz'), '-inf Hz'),
    Case('outcome', '-$inf', ('-inf', '$'), '-$inf'),
    Case('baroness', 'nan', ('nan', ''), 'nan'),
    Case('province', 'nan Hz', ('nan', 'Hz'), 'nan Hz'),
    Case('infidel', '$nan', ('nan', '$'), '$nan'),
    Case('honey', '+nan', ('nan', ''), 'nan'),
    Case('frighten', '+nan Hz', ('nan', 'Hz'), 'nan Hz'),
    Case('acrobat', '+$nan', ('nan', '$'), '$nan'),
    Case('firefly', 'INF', ('inf', ''), 'inf'),
    Case('farmland', 'INF Hz', ('inf', 'Hz'), 'inf Hz'),
    Case('osteopath', '$INF', ('inf', '$'), '$inf'),
    Case('chickpea', '-INF', ('-inf', ''), '-inf'),
    Case('bawdy', '-INF Hz', ('-inf', 'Hz'), '-inf Hz'),
    Case('pursuer', '-$INF', ('-inf', '$'), '-$inf'),
    Case('suffuse', 'NAN', ('nan', ''), 'nan'),
    Case('vacillate', 'NAN Hz', ('nan', 'Hz'), 'nan Hz'),
    Case('tangerine', '$NAN', ('nan', '$'), '$nan'),
    Case('southward', '+NAN', ('nan', ''), 'nan'),
    Case('wander', '+NAN Hz', ('nan', 'Hz'), 'nan Hz'),
    Case('stack', '+$NAN', ('nan', '$'), '$nan'),

    # test full precision
    Case('cauldron', '1420.405751786 MHz', ('1.420405751786e9', 'Hz'), '1.420405751786GHz', {'prec':'full'}),
    Case('fiery', '3.14159265ns', ('3.14159265e-9', 's'), '3.14159265ns', {'prec':'full'}),
    Case('magnate', '3.14159265 ns', ('3.14159265e-9', 's'), '3.14159265ns', {'prec':'full'}),
    Case('canard', '3.141592650ns', ('3.14159265e-9', 's'), '3.14159265ns', {'prec':'full'}),
    Case('clothe', '3.1415926500ns', ('3.14159265e-9', 's'), '3.14159265ns', {'prec':'full'}),
    Case('texture', '.314159265ns', ('314.159265e-12', 's'), '314.159265ps', {'prec':'full'}),
    Case('escalate', '.314159265 ns', ('314.159265e-12', 's'), '314.159265ps', {'prec':'full'}),
    Case('raise', '.3141592650ns', ('314.159265e-12', 's'), '314.159265ps', {'prec':'full'}),
    Case('campsite', '.31415926500ns', ('314.159265e-12', 's'), '314.159265ps', {'prec':'full'}),
    Case('whodunit', '0.314159265ns', ('314.159265e-12', 's'), '314.159265ps', {'prec':'full'}),
    Case('limerick', '0.314159265 ns', ('314.159265e-12', 's'), '314.159265ps', {'prec':'full'}),
    Case('moped', '0.3141592650ns', ('314.159265e-12', 's'), '314.159265ps', {'prec':'full'}),
    Case('layette', '0.31415926500ns', ('314.159265e-12', 's'), '314.159265ps', {'prec':'full'}),
    Case('luncheon', '.0314159265ns', ('31.4159265e-12', 's'), '31.4159265ps', {'prec':'full'}),
    Case('abyss', '.0314159265 ns', ('31.4159265e-12', 's'), '31.4159265ps', {'prec':'full'}),
    Case('daylight', '.0314159265ns', ('31.4159265e-12', 's'), '31.4159265ps', {'prec':'full'}),
    Case('jackpot', '.0314159265ns', ('31.4159265e-12', 's'), '31.4159265ps', {'prec':'full'}),
    Case('gelding', '0.0314159265ns', ('31.4159265e-12', 's'), '31.4159265ps', {'prec':'full'}),
    Case('sliver', '0.0314159265ns', ('31.4159265e-12', 's'), '31.4159265ps', {'prec':'full'}),
    Case('turquoise', '0.0314159265ns', ('31.4159265e-12', 's'), '31.4159265ps', {'prec':'full'}),
    Case('astonish', '0.0314159265ns', ('31.4159265e-12', 's'), '31.4159265ps', {'prec':'full'}),
    Case('reverie', '.00314159265ns', ('3.14159265e-12', 's'), '3.14159265ps', {'prec':'full'}),
    Case('angreal', '.00314159265ns', ('3.14159265e-12', 's'), '3.14159265ps', {'prec':'full'}),
    Case('rewire', '.00314159265ns', ('3.14159265e-12', 's'), '3.14159265ps', {'prec':'full'}),
    Case('promise', '.00314159265ns', ('3.14159265e-12', 's'), '3.14159265ps', {'prec':'full'}),
    Case('harmonica', '0.00314159265ns', ('3.14159265e-12', 's'), '3.14159265ps', {'prec':'full'}),
    Case('flashcard', '0.00314159265ns', ('3.14159265e-12', 's'), '3.14159265ps', {'prec':'full'}),
    Case('sediment', '0.00314159265ns', ('3.14159265e-12', 's'), '3.14159265ps', {'prec':'full'}),
    Case('cleanser', '0.00314159265ns', ('3.14159265e-12', 's'), '3.14159265ps', {'prec':'full'}),

    # test full precision
    Case('chestnut', '1 ns', ('1e-9', 's'), '1ns', {'strip_radix':True}),
    Case('alpha', '1 s', ('1', 's'), '1s', {'strip_radix':True}),
    Case('parka', '1 ns', ('1e-9', 's'), '1n', {'strip_radix':False, 'show_units':False}),
    Case('creeper', '1 s', ('1.0', 's'), '1.0', {'strip_radix':False, 'show_units':False}),
    Case('walkabout', '1 ns', ('1e-9', 's'), '1n', {'strip_radix':False, 'prec':'full', 'show_units':False}),
    Case('substance', '1 s', ('1.0', 's'), '1.0', {'strip_radix':False, 'prec':'full', 'show_units':False}),

    # test preferences
    Case('flotation', '1420.405751786 MHz', ('1e9', 'Hz'), '1GHz', {'prec':0}),
    Case('bodyguard', '1420.405751786 MHz', ('1.4e9', 'Hz'), '1.4GHz', {'prec':1}),
    Case('radiogram', '1420.405751786 MHz', ('1.42e9', 'Hz'), '1.42GHz', {'prec':2}),
    Case('omnibus', '1420.405751786 MHz', ('1.42e9', 'Hz'), '1.42GHz', {'prec':3}),
    Case('transmit', '1420.405751786 MHz', ('1.4204e9', 'Hz'), '1.4204GHz', {'prec':4}),
    Case('morality', '1420.405751786 MHz', ('1.42041e9', 'Hz'), '1.42041GHz', {'prec':5}),
    Case('reward', '1420.405751786 MHz', ('1.420406e9', 'Hz'), '1.420406GHz', {'prec':6}),
    Case('smudge', '1420.405751786 MHz', ('1.4204058e9', 'Hz'), '1.4204058GHz', {'prec':7}),
    Case('animator', '1420.405751786 MHz', ('1.42040575e9', 'Hz'), '1.42040575GHz', {'prec':8}),
    Case('woodwind', '1420.405751786 MHz', ('1.420405752e9', 'Hz'), '1.420405752GHz', {'prec':9}),
    Case('underpay', '1420.405751786 MHz', ('1.4204057518e9', 'Hz'), '1.4204057518GHz', {'prec':10}),
    Case('horoscope', '1420.405751786 MHz', ('1.42040575179e9', 'Hz'), '1.42040575179GHz', {'prec':11}),
    Case('drivel', '1420.405751786 MHz', ('1.420405751786e9', 'Hz'), '1.420405751786GHz', {'prec':12}),
    Case('railcard', '1420.405751786 MHz', ('1.420405751786e9', 'Hz'), '1.420405751786GHz', {'prec':13}),
    Case('elixir', '1420.405751786 MHz', ('1.4204e9', 'Hz'), '1.4204 GHz', {'prec':None, 'spacer':' '}),
    Case('henna', '3.141592 Hz', ('3.1416', 'Hz'), '3.1416_Hz', {'unity_sf':'_', 'spacer':''}),
    Case('eastward', '3.141592 Hz', ('3.1416', 'Hz'), '3.1416 Hz', {'spacer':' '}),
    Case('string', '1420.405751786MHz', ('1.4204e9', 'Hz'), '1.4204e9Hz', {'output_sf':''}),
    Case('airliner', '1ns', ('1', 'ns'), '1ns', {'ignore_sf':True}),
    Case('anchorage', '1000 MHz', ('1e9', 'Hz'), '1GHz', dict(prec=0, strip_zeros=False)),
    Case('moorland', '1000 MHz', ('1e9', 'Hz'), '1GHz', dict(prec=0, strip_zeros=True)),
    Case('rinse', '1000 MHz', ('1.0e9', 'Hz'), '1.0GHz', dict(prec=1, strip_zeros=False)),
    Case('drugstore', '1000 MHz', ('1e9', 'Hz'), '1GHz', dict(prec=1, strip_zeros=True)),
    Case('aspen', '1000 MHz', ('1.00e9', 'Hz'), '1.00GHz', dict(prec=2, strip_zeros=False)),
    Case('resolve', '1000 MHz', ('1e9', 'Hz'), '1GHz', dict(prec=2, strip_zeros=True)),
    Case('cultivate', '1000 MHz', ('1.000e9', 'Hz'), '1.000GHz', dict(prec=3, strip_zeros=False)),
    Case('mantis', '1000 MHz', ('1e9', 'Hz'), '1GHz', dict(prec=3, strip_zeros=True)),
]

names = set()
def test_number_recognition():
    Quantity.set_prefs(spacer=None, show_label=None, label_fmt=None, label_fmt_full=None)
    for case in test_cases:
        if not case:
            continue
        assert case.name not in names, '%s: duplicate test name' % case.name
        names.add(case.name)

        Quantity.set_prefs(
            prec=None, full_prec=None, spacer='', unity_sf=None, output_sf=None,
            ignore_sf=None, label_fmt=None, assign_rec=None, show_units=True,
            strip_radix=True, strip_zeros=True
        )
        try:
            if case.prefs:
                Quantity.set_prefs(**case.prefs)
            q = Quantity(case.text)
            assert ((q.render(show_si=False, show_units=False), q.units) == case.raw), case.name
            assert (str(q) == case.formatted), case.name
            # assure that the output value can be read as an input
            Quantity(str(q))
        except AssertionError:
            raise
        except (ValueError, KeyError):
            assert None is case.raw, case.name
        except Exception:
            print('%s: unexpected exception occurred.' % case.name)
            raise
    Quantity.set_prefs(
        prec=None, full_prec=None, spacer=None, unity_sf=None, output_sf=None,
        ignore_sf=None, label_fmt=None, assign_rec=None
    )
