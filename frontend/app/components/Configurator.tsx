'use client';

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { StepOne } from './steps/StepOne';
import { StepTwo } from './steps/StepTwo';
import { StepThree } from './steps/StepThree';
import { StepFour } from './steps/StepFour';
import { Preview } from './Preview';
import { CheckCircle2, ChevronRight, ChevronLeft, AlertCircle, Loader2 } from 'lucide-react';
import { calculateConfiguration, createOrder, getMaterials, getBlindsTypes } from '@/lib/api';
import type { ConfigurationResponse, Material, BlindsType } from '@/lib/api';

export function Configurator() {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [config, setConfig] = useState({
    type: 'horizontal',
    width: 100,
    height: 100,
    material: 'aluminum',
    color: '#ffffff',
    texture: 'matte',
    control: 'manual',
    options: [],
  });

  const [pricing, setPricing] = useState<ConfigurationResponse | null>(null);
  const [materials, setMaterials] = useState<Material[]>([]);
  const [blindsTypes, setBlindsTypes] = useState<BlindsType[]>([]);

  const steps = [
    { id: 'type', number: 1, title: 'Тип жалюзи', component: StepOne },
    { id: 'size', number: 2, title: 'Размеры', component: StepTwo },
    { id: 'material', number: 3, title: 'Материал & Цвет', component: StepThree },
    { id: 'options', number: 4, title: 'Опции & Итого', component: StepFour },
  ];

  const CurrentStep = steps[step - 1]?.component;

  // Load initial data
  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        const [materialsRes, typesRes] = await Promise.all([
          getMaterials(),
          getBlindsTypes(),
        ]);

        if (materialsRes.success && materialsRes.data) {
          setMaterials(materialsRes.data);
        }
        if (typesRes.success && typesRes.data) {
          setBlindsTypes(typesRes.data);
        }
      } catch (err) {
        console.error('Error loading data:', err);
        setError('Ошибка загрузки данных');
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  // Calculate pricing when configuration changes
  useEffect(() => {
    const calculatePrice = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Get material ID from selected material name
        const selectedMaterial = materials.find(m => m.name === config.material);
        if (!selectedMaterial) {
          setError('Материал не найден');
          return;
        }

        const result = await calculateConfiguration({
          blinds_type: config.type,
          material_id: selectedMaterial.id,
          control_type: config.control,
          width_mm: config.width,
          height_mm: config.height,
          quantity: 1,
          custom_options: config.options?.length > 0 ? { options: config.options } : undefined,
        });

        if (result.success && result.data) {
          setPricing(result.data);
          setError(null);
        } else {
          setError(result.error || 'Ошибка расчета цены');
        }
      } catch (err) {
        console.error('Error calculating price:', err);
        setError('Ошибка при расчете цены');
      } finally {
        setLoading(false);
      }
    };

    // Debounce calculation
    const timer = setTimeout(calculatePrice, 500);
    return () => clearTimeout(timer);
  }, [config, materials]);

  // Validation
  const isConfigValid = () => {
    return (
      config.type &&
      config.width > 0 &&
      config.height > 0 &&
      config.material &&
      config.color &&
      config.control &&
      pricing &&
      !error
    );
  };

  const handleCreateOrder = async () => {
    if (!isConfigValid()) {
      setError('Пожалуйста, заполните все обязательные поля');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const selectedMaterial = materials.find(m => m.name === config.material);
      if (!selectedMaterial) {
        setError('Материал не найден');
        return;
      }

      // For now, use a test client ID. In real app, get from auth context
      const CLIENT_ID = 1;

      const result = await createOrder({
        client_id: CLIENT_ID,
        order_items: [
          {
            width_mm: config.width,
            height_mm: config.height,
            blinds_type: config.type,
            material_id: selectedMaterial.id,
            control_type: config.control,
            quantity: 1,
            custom_options: config.options?.length > 0 ? { options: config.options } : undefined,
          },
        ],
        notes: 'Заказ из конфигуратора',
      });

      if (result.success) {
        alert('✅ Заказ успешно создан!');
        // Reset form
        setStep(1);
        setConfig({
          type: 'horizontal',
          width: 100,
          height: 100,
          material: 'aluminum',
          color: '#ffffff',
          texture: 'matte',
          control: 'manual',
          options: [],
        });
        setPricing(null);
      } else {
        setError(result.error || 'Ошибка при создании заказа');
      }
    } catch (err) {
      console.error('Error creating order:', err);
      setError('Ошибка при создании заказа');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
      {/* Main Content */}
      <div className="lg:col-span-2">
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-8">
          {/* Error Message */}
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3"
            >
              <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
              <p className="text-red-700 text-sm">{error}</p>
            </motion.div>
          )}

          {/* Steps Indicator */}
          <div className="flex items-center justify-between mb-12">
            {steps.map((s, index) => (
              <React.Fragment key={s.id}>
                <motion.div
                  whileHover={{ scale: 1.05 }}
                  onClick={() => setStep(s.number)}
                  className={`flex items-center justify-center w-10 h-10 rounded-full font-medium cursor-pointer transition-all ${
                    step >= s.number
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-500'
                  }`}
                >
                  {step > s.number ? <CheckCircle2 className="w-5 h-5" /> : s.number}
                </motion.div>
                {index < steps.length - 1 && (
                  <div
                    key={`line-${s.id}`}
                    className={`flex-1 h-1 mx-2 ${step > s.number ? 'bg-blue-600' : 'bg-gray-100'}`}
                  />
                )}
              </React.Fragment>
            ))}
          </div>

          {/* Step Title */}
          <motion.div
            key={`title-${step}`}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-8"
          >
            <h2 className="text-2xl font-bold text-gray-900">{steps[step - 1]?.title}</h2>
          </motion.div>

          {/* Step Content */}
          <motion.div
            key={`content-${step}`}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
          >
            {CurrentStep && (
              <CurrentStep 
                config={config} 
                setConfig={setConfig}
                materials={materials}
                blindsTypes={blindsTypes}
              />
            )}
          </motion.div>

          {/* Navigation */}
          <div className="flex justify-between mt-12">
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => setStep(Math.max(1, step - 1))}
              disabled={step === 1 || loading}
              className="flex items-center gap-2 px-6 py-3 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <ChevronLeft className="w-4 h-4" />
              Назад
            </motion.button>

            {step < 4 ? (
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => setStep(Math.min(4, step + 1))}
                disabled={loading}
                className="flex items-center gap-2 px-6 py-3 text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {loading && <Loader2 className="w-4 h-4 animate-spin" />}
                Далее
                <ChevronRight className="w-4 h-4" />
              </motion.button>
            ) : (
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={handleCreateOrder}
                disabled={!isConfigValid() || loading}
                className="flex items-center gap-2 px-6 py-3 text-white bg-green-600 rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {loading && <Loader2 className="w-4 h-4 animate-spin" />}
                Создать заказ
                <CheckCircle2 className="w-4 h-4" />
              </motion.button>
            )}
          </div>
        </div>
      </div>

      {/* Preview & Summary */}
      <div>
        <Preview config={config} pricing={pricing} loading={loading} />
      </div>
    </div>
  );
}
